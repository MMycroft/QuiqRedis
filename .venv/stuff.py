import sys

class Redis:
    """Redis Class"""
    commands: dict = {
    'HELP': 'help',
    'COMMANDS': 'commands',
    'SET':  'set',
    'GET':  'get',
    'MGET': 'm_get',
    'KEYS': 'keys',
    'EXISTS': 'exists',
    'DEL': 'delete',
    'INCR':  'increment',
    'LPUSH': 'left_push',
    'RPUSH': 'right_push',
    'LPOP': 'left_pop',
    'RPOP': 'right_pop',
    'LRANGE': 'list_range',
    'LLEN': 'list_length',
    'HSET': 'hash_set',
    'HGET': 'hash_get',
    'HGETALL': 'hash_get_all',
    'END': 'end',
    'DEFAULT': 'default'
    }


    def __init__(self, username: str = 'default'):
        """ Redis class constructor"""
        self.username: str = username
        self.flag: bool = True
        self.data: dict[str, str] = {}

    @classmethod
    def get_command(cls, com):
        """gets commands"""
        command = cls.commands.get(com, default = 'default')
        command = command if hasattr(Redis, command) else 'default'
        return getattr(Redis, com)

    @classmethod
    def execute_command(cls, com: str, args: list):
        """executes commands"""
        command = Redis.get_command(com)
        command(args)

    @classmethod
    def help(cls, args: list[str]):
        """helps out"""
        command = args[0].upper()
        print(Redis.get_command(command).__doc__)

    @classmethod
    def commands(cls, self):
        """Does stuff"""
        for key in self.command_funcs.keys():
            print(key)

    def end(self):
        """ends program"""
        self.flag = False

    @classmethod
    def default(cls):
        """default"""
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

        redis.execute_command(com, args)


if __name__ == "__main__":
    main()