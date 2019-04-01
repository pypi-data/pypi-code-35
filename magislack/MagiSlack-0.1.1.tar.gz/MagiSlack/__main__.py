from os import environ
from random import randint

from MagiSlack.io import MagiIO
from MagiSlack.module import MagiModule


def hello_world(*args, **kwargs):
    return f"HELLO WORLD! user {kwargs['name']}, {kwargs['display_name']}"

def random(*args, **kwargs):
    for a in args:
        print(a)
    number = randint(int(args[0]), int(args[1]))
    return f"You got {number}!"

if __name__ == '__main__':
    print('Magi Start!')
    print('='*30)
    print('MagiModule Initializing.')
    module = MagiModule.MagiModule(environ['SLACK_API_TOKEN'])
    print('Complete')

    print('='*30)
    print('MagiIO Initializing.')
    io = MagiIO.MagiIO(module)
    print('Complete')
    print('='*30)

    io.set_callback_func('hello', hello_world)
    io.set_callback_func('random', random)

    io.start()
