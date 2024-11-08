import sys, time
from unittest import case


class Redis:
    """Redis Class"""
    def __init__(self):
        """ Redis Class Constructor"""
        self.active: bool = True        # active indicates the program should continue
        self.data: dict[str,str] = {}            # stores Redis key values
        self.lifetimes: dict[str,float] = {}     # stores Redis key lifetimes
        self.commands: dict[str,callable] = {    # maps command string to command function
                'HELP': self.redis_help,
                'SET': self.redis_set,
                'GET': self.redis_get,
                'MGET': self.redis_mget,
                'DEL': self.redis_delete,
                'LPUSH': self.redis_left_push,
                'LPOP': self.redis_left_pop,
                'LRANGE': self.redis_range,
                'HSET': self.redis_hash_set,
                'HGET': self.redis_hash_get,
                'END': self.redis_end
        }

    def clean(self):
        """
        Removes any keys beyond expiration time from data set and lifetimes set.
        """
        keys: list[str] = list(self.lifetimes.keys())       # list of keys with active lifetimes (may be empty)
        for key in keys:
            if time.time() > self.lifetimes.get(key, 0.):   # check if time has expired
                self.data.pop(key, '')                      # remove from data FIRST
                self.lifetimes.pop(key, '')                 # remove from lifetimes set LAST

    def execute_command(self, com: str, args: list):
        """
        param com: Redis command string
        param args: Arguments for command function

        Executes appropriate command function with args list
        """
        command: callable = self.commands.get(com.upper(), self.redis_default)    # get command function
        print(command(args))

    def redis_help(self, args: list[str]):
        """
        Returns doc strings for functions associated with provided Redis command strings
        If no commands are provided, all commands are printed out.

        param args: List of Redis command strings.
        """
        # list of command strings ['get', 'SET', 'Help']
        command_strings: list[str] = args if len(args) > 0 else list(self.commands.keys())
        # list of command strings concatenated to their doc strings
        result: list[str] = []
        for com in command_strings:
            com_string: str = com.upper()
            command: callable = self.commands.get(com_string, self.redis_default)
            doc_string = command.__doc__
            result.append(com_string + doc_string)

        return '\n'.join(result)

    def redis_set(self, args: list[str]):
        """
        Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type.
        Any previous time to live associated with the key is discarded on successful SET operation.

        The SET command supports a set of options that modify its behavior:
            EX seconds -- Set the specified expire time, in seconds (a positive integer).
            PX milliseconds -- Set the specified expire time, in milliseconds (a positive integer).
            EXAT timestamp-seconds -- Set the specified Unix time at which the key will expire, in seconds (a positive integer).
            PXAT timestamp-milliseconds -- Set the specified Unix time at which the key will expire, in milliseconds (a positive integer).
            NX -- Only set the key if it does not already exist.
            XX -- Only set the key if it already exists.
            KEEPTTL -- Retain the time to live associated with the key.
            GET -- Return the old string stored at key, or nil if key did not exist.
                   An error is returned and SET aborted if the value stored at key is not a string.

        param args: ['key', 'value', options = ['NX' | 'XX'] ['GET'] ['EX' 'seconds' | 'PX' 'milliseconds' | 'EXAT' 'unix-time-seconds' | 'PXAT' 'unix-time-milliseconds' | 'KEEPTTL'] ]

        Nil reply: GET not given: Operation was aborted (conflict with one of the XX/NX options).
        Simple string reply: OK. GET not given: The key was set.
        Nil reply: GET given: The key didn't exist before the SET.
        Bulk string reply: GET given: The previous value of the key.

        """
        if len(args) < 2:
            return "ERROR wrong number of arguments"

        insert = True
        key, value, *opts = args

        result = 'OK'
        current_lifetime = self.lifetimes.pop(key, 0.)
        while len(opts) > 0:
            match opts.pop(0).upper():
                case 'NX':
                    if key in self.data: insert = False
                case 'XX':
                    if insert == False: return "ERROR syntax error"
                    if key not in self.data: insert = False
                case 'GET':
                    result = self.redis_get([key])
                case 'EX':
                    if opts[0].isdigit():
                        expire = time.time() + float(opts.pop(0))
                        self.lifetimes[key] = expire
                    else:
                        insert = False
                case 'PX':
                    if opts[0].isdigit():
                        expire = time.time() + float(opts.pop(0))/1000
                        self.lifetimes[key] = expire
                    else:
                        insert = False
                case 'EXAT':
                    if opts[0].isdigit():
                        expire = float(opts.pop(0))
                        self.lifetimes[key] = expire
                    else:
                        insert = False
                case 'PXAT':
                    if opts[0].isdigit():
                        expire = float(opts.pop(0))/1000
                        self.lifetimes[key] = expire
                    else:
                        insert = False
                case 'KEEPTTL':
                    self.lifetimes[key] = current_lifetime
                case _:
                    return "ERROR unknown option"

        if insert:
            self.data[key] = value
            return result
        else:
            return ''


    def redis_get(self, args: list[str]):
        """
        Get the value of key. If the key does not exist the special value nil is returned.
        An error is returned if the value stored at key is not a string, because GET only handles string values.
        Ignores trailing arguments.

        param args: [key]

        Bulk string reply: the value of the key.
        Nil reply: if the key does not exist.
        """
        if len(args) > 0:
            key = args[0]
            value = self.data.get(key, 'nil')
            return (f'{value}' if isinstance(value, str) else "ERROR not a string").strip()

    def redis_mget(self, args: list[str]):
        """
        Returns the values of all specified keys. For every key that does not hold a string value or does not exist,
        the special value nil is returned. Because of this, the operation never fails. Supports multiple inputs.

        param args: [key, key, key, ...]

        Array reply: a list of values at the specified keys.
        """
        result = []
        for i, key in enumerate(args):
            value = self.data.get(key, 'nil')
            result.append("%-5d" % (i + 1) + f'{value}')
        return '\n'.join(result).strip()

    def redis_delete(self, args: list[str]):
        """
        Removes the specified keys. A key is ignored if it does not exist.

        param args: [key, key, key, ...]

        Integer reply: the number of keys that were removed.
        """
        count=0
        for arg in args: count += 1 if self.data.pop(arg, None) is not None else 0
        return f'integer {count}'

    def redis_left_push(self, args: list[str]):
        """
        Insert all the specified values at the head of the list stored at key.
        If key does not exist, it is created as empty list before performing the push operations.
        When key holds a value that is not a list, an error is returned.

        It is possible to push multiple elements using a single command call just specifying multiple arguments
        at the end of the command. Elements are inserted one after the other to the head of the list, from the
        leftmost element to the rightmost element.

        param args: [key, element, element, element, ...]

        Integer reply: the length of the list after the push operation.
        """
        name, *elements = args
        value = self.data.get(name, [])
        if isinstance(value, list):
            elements.reverse()
            self.data[name] = [*elements, *value]
            return 'integer ' + str(len(self.data[name]))
        else:
            return "ERROR not a list"

    def redis_left_pop(self, args: list[str]):
        """
        Removes and returns the first elements of the list stored at key.

        By default, the command pops a single element from the beginning of the list.
        When provided with the optional count argument, the reply will consist of up
        to count elements, depending on the list's length.

        Nil reply: if the key does not exist.
        Bulk string reply: when called without the count argument, the value of the first element.
        Array reply: when called with the count argument, a list of popped elements.

        param args: [key, count]
        """

        match len(args):
            case 0:
                return "ERROR not enough arguments"
            case 1: name, count = args[0], '1'
            case _: name, count = args[0], args[1]

        count = int(count) if count.isdigit() else 0
        value_list = self.data.get(name, None)

        if isinstance(value_list, list):
            removed, remainder = self.data[name][:count], self.data[name][count:]
            self.data[name] = remainder
            return 'integer ' + str(len(removed))
        else:
            return "ERROR: not a list"

    def redis_range(self, args: list[str]):
        """
        Returns the specified elements of the list stored at key.
        The offsets start and stop are zero-based indexes, with 0 being the first element of the list
        (the head of the list), 1 being the next element and so on.

        These   offsets can also be negative numbers indicating offsets starting at the end of the list.
        For example, -1 is the last element of the list, -2 the penultimate, and so on.

        param args: ['key', 'start', 'stop']
        """
        if len(args) < 3:
            return "ERROR not enough arguments"

        def get_num(number: str):
            if number[0] == '-':
                mult: int = -1
                num = int(number[1:]) if number[1:].isdigit() else None
            else:
                mult: int = 1
                num = int(number) if number.isdigit() else None
            return None if num is None else num * mult

        name =  args[0]
        start = get_num(args[1])
        end = get_num(args[2])

        if start is None or end is None: return "ERROR not an integer"

        value: list = self.data.get(name, [])

        if isinstance(value, list):
            result = []
            if end < 0:
                end += len(value)
            if end >= len(value): end = len(value) - 1
            for i in range(start, end + 1):
                result.append("%-5d" % (i + 1) + f'{value[i]}')
            return '\n'.join(result).strip()
        else:
            return "ERROR not a list"

    def redis_hash_set(self, args: list[str]):
        """
        Sets the specified fields to their respective values in the hash stored at key.
        This command overwrites the values of specified fields that exist in the hash.
        If key doesn't exist, a new key holding a hash is created.
        Accepts multiple field and value arguments.
        Ignores trailing field if no value is specified.
        Empty fields are not permitted.

        param args: ['key', 'field', 'value', ...]

        Integer reply: the number of fields that were added.
        """
        if len(args) < 3:
            return "ERROR: not enough arguments"


        key, *elements = args

        value = self.data.get(key, {})

        if isinstance(value, dict):
            if len(value) == 0: self.data[key] = {}
            if len(elements) % 2 == 1: elements.pop()

            for i in range(0, len(elements), 2):
                self.data[key][elements[i]] = elements[i + 1]
            return "integer " + str((i + 2) // 2)

        else:
            return "ERROR: not a hash set"

    def redis_hash_get(self, args: list[str]):
        """
        Returns the value associated with field in the hash stored at key.
        Does not support multiple field values. Ignores trailing arguments.

        param args: ['key', 'field']

        Bulk string reply: The value associated with the field.
        Nil reply: If the field is not present in the hash or key does not exist.
        """
        if len(args) < 2:
            return "ERROR not enough arguments"

        name, key = args[0], args[1]
        hash = self.data.get(name, 'nil')
        if isinstance(hash, dict):
            value = hash.get(key, 'nil')
            return f'{value}'
        elif hash == 'nil':
            return 'nil'
        else:
            return "ERROR not a hash set"



    def redis_default(self, *_):
        """
        not a command
        """
        return "ERROR not a command"

    def redis_end(self, *_):
        """
        Terminates the Quiq Redis CLI
        """
        self.flag = False
        return 'THE END'



def main():
    redis = Redis()

    print("------------------------------------------------------")
    print("                    QUIQ REDIS CLI                    ")
    print("------------------------------------------------------")
    print("Enter HELP to see all commands with descriptions")
    print("Enter HELP <command> to see a description of a command")
    print("Enter END to terminate the program")
    print("------------------------------------------------------")

    while redis.active:
        print("command> ", end='')
        in_str: str = input()
        com, *args = in_str.split(' ')
        redis.clean()
        redis.execute_command(com, args)

if __name__ == "__main__":
    main()