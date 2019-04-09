## GYNX settings ##
import os

# Set environment
ENVIRONMENT = 'master'

live = True if ENVIRONMENT == 'live' or ENVIRONMENT == 'master' else False

# Base settings variables (environment specific)

class Settings(object):

    def __init__(self, environment, *args, **kwargs):
        self.environment = environment

    @property
    def DEBUG(self):
        return False if self.environment == 'live' else True

    @property
    def DIRECTORY(self):
        testdrive = os.path.join(os.getcwd(), 'tests', 'drive/')
        return os.getcwd() + '/' if self.environment == 'live' else testdrive

    @property
    def TOKEN_FILE(self):
        return 'token.json' if self.environment == 'live' else 'test.json'

test_environment = Settings('test')
live_environment = Settings('live')

environment = live_environment if live else test_environment
