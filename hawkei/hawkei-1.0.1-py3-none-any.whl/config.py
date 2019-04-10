from hawkei.utils import merge

_DEFAULT_OBFUSCATED_FIELDS = [
    'password',
    'password_confirmation',
    'secret',
    'secret_token',
    'authenticity_token',
    'token',
    'api_key',
    'access_token',
    'credit_card_number',
    'cvv',
    'ccv',
    'csrfmiddlewaretoken',
]

_DEFAULT = {
    'api_key': None,
    'space_name': None,
    'environment_name': None,
    'api_host': 'https://api.hawkei.io',
    'api_version': 'v1',
    'enabled': True,
    'obfuscated_fields': [],
    'metadata': {},
    'domain': None,
}

class Config():

    def __init__(self):
        self.data = None

    def build(self, user_config):
        self.data = merge(_DEFAULT, user_config)
        self.data['obfuscated_fields'] += _DEFAULT_OBFUSCATED_FIELDS
        self.validate()

    def active(self):
        if not self.data:
            return False

        return self.data['enabled']

    def validate(self):
        self.require('api_key', str)
        self.require('space_name', str)
        self.require('environment_name', str)
        self.require('api_host', str)

    def require(self, field, field_type):
        value = self.data[field]

        if not isinstance(value, field_type):
            message = 'Invalid configuration for field: {0}'.format(field)
            raise AssertionError(message)

config = Config()
