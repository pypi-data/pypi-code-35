from decouple import config


class GwapAuthSettings:
    TOKEN_URL = config('TOKEN_URL')
    AUTHORIZE_URL = config('AUTHORIZE_URL')
    INTROSPECT_URL = config('INTROSPECT_URL')
    TOKEN_KEY = config('TOKEN_KEY')
