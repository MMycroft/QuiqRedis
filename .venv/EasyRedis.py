import sys

class Redis:

    def __init__(self, username: str = 'default'):
        self.username: str = username
        self.flag: bool = True
        self.data: dict[str, str] = {}
        self.command_funcs = {
            'HELP': Redis.help,
            'COMMANDS': Redis.commands,
            'SET': Redis.set,
            'GET': Redis.get,
            'MGET': Redis.m_get,
            'KEYS': Redis.keys,
            'EXISTS': Redis.exists,
            'DEL': Redis.delete,
            'INCR': Redis.increment,
            'LPUSH': Redis.left_push,
            'RPUSH': Redis.right_push,
            'LPOP': Redis.left_pop,
            'RPOP': Redis.right_pop,
            'LRANGE': Redis.list_range,
            'LLEN': Redis.list_length,
            'HSET': Redis.hash_set,
            'HGET': Redis.hash_get,
            'HGETALL': Redis.hash_get_all,
            'END': Redis.end
        }

    def get_command(self, com):
        return self.command_funcs.get(com, Redis.default)

    def execute_command(self, com: str, args: list):
        command = self.get_command(com)
        command(self, args)

    def help(self, args: list[str]):
        """helps out"""
        command = args[0].upper()
        print(self.get_command(command).__doc__)

    def commands(self):
        """Does stuff"""
        for key in self.command_funcs.keys():
            print(key)

    def set(self, args):
        self.data[args[0]] = args[1]

    def get(self):
        print('get')

    def m_get(self):
        print('m_get')

    def keys(self):
        print('keys')

    def exists(self):
        print('exists')

    def delete(self):
        print('delete')

    def increment(self):
        print('increment')

    def left_push(self):
        print('left_push')

    def right_push(self):
        print('right_push')

    def left_pop(self):
        print('left_pop')

    def right_pop(self):
        print('right_pop')

    def list_range(self):
        print('list_range')

    def list_length(self):
        print('list_length')

    def hash_set(self):
        print('hash_set')

    def hash_get(self):
        print('hash_get')

    def hash_get_all(self):
        print('hash_get_all')

    def end(self):
        self.flag = False

    def default():
        print('default')




def main():
    args = sys.argv

    username = args[0] if args[0] else 'default'

    redis = Redis(username)

    print("QUIQ REDIS")
    print("Enter COMMANDS to see all commands")
    print("Enter HELP <command> to see a description of a command")


    while redis.flag:
        in_str: str = input("command> ")
        inputs = in_str.split(' ')

        com = inputs[0].upper()
        args = inputs[1:]

        print(com)
        print(args)

        redis.execute_command(com, args)


if __name__ == "__main__":
    main()



    def matches(self, com: str, args: list):
        match com:
            case 'HELP':
                Redis.help(args),
            case 'COMMANDS':
                Redis.commands(args),
            case 'SET':
                Redis.set(args),
            case 'GET':
                Redis.get(args),
            case 'MGET':
                Redis.m_get(args),
            case 'KEYS':
                Redis.keys(args),
            case 'EXISTS':
                Redis.exists(args),
            case 'DEL':
                Redis.delete(args),
            case 'INCR':
                Redis.increment(args),
            case 'LPUSH':
                Redis.left_push(args),
            case 'RPUSH':
                Redis.right_push(args),
            case 'LPOP':
                Redis.left_pop(args),
            case 'RPOP':
                Redis.right_pop(args),
            case 'LRANGE':
                Redis.list_range(args),
            case 'LLEN':
                Redis.list_length(args),
            case 'HSET':
                Redis.hash_set(args),
            case 'HGET':
                Redis.hash_get(args),
            case 'HGETALL':
                Redis.hash_get_all(args),
            case 'END':
                Redis.end(args),
            case _:
                Redis.default(args)