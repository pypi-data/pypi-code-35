import os

PRODUCTION = os.environ.get('PRODUCTION', False)

AMY = os.environ.get('AMY', 'amy')
AMY_Q = os.environ.get('AMY_Q', AMY)
AMY_Q_HOST = os.environ.get(
    'AMY_Q_HOST', AMY + '-q') if PRODUCTION else 'localhost'

AMY_HASHKEY = os.environ.get('AMY_HASHKEY','9x6E0irEEI5BcVRPiavbbdSdJZwaHDegtIkRqH1QdzY=')
