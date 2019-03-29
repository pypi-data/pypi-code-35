from datetime import datetime
from starlette.config import Config
from starlette.datastructures import Secret, URL
from databases import DatabaseURL

module_config = Config(env_file='/.env.registration')
database_config = Config(env_file='/.env.database')
smtp_config = Config(env_file='/.env.smtp')

### Module configuration
TESTING = module_config('TESTING', cast=bool, default='false')
DEBUG = module_config('DEBUG', cast=bool, default='false')
DATE_REGISTRATION_END = datetime.strptime(module_config('DATE_REGISTRATION_END', default='2019-05-24'), '%Y-%m-%d')
URL_NOT_FOUND_PAGE = module_config('URL_NOT_FOUND_PAGE', cast=URL, default='https://wmgames.ee/404')
# Base URL of confirmation endpoint
URL_CONFIRM_BASE = module_config('URL_CONFIRM_BASE', cast=URL, default='https://wmgames.ee/confirm')
# Page that greets new participant, universal for everybody and without personal data
URL_WELCOME_PAGE = module_config('URL_WELCOME_PAGE', cast=URL, default='https://wmgames.ee/welcome')
RECAPTCHA_DISABLE = module_config('RECAPTCHA_DISABLE', cast=bool, default='true')
RECAPTCHA_SECRET_KEY = module_config('RECAPTCHA_SECRET_KEY', cast=Secret, default='change-me-please')
CONFIRMATION_FROM = module_config('CONFIRMATION_FROM', default='Worldman Games <info@wmgames.ee>')
# Secret combination that is used when creating confirmation code
CONFIRMATION_SECRET = module_config('CONFIRMATION_SECRET', cast=Secret, default='change-me-please')
DATABASE_PARTICIPANTS_TABLE = module_config('DATABASE_PARTICIPANTS_TABLE', default='participants_2019_1')

### Database configuration
DATABASE_URL = database_config('DATABASE_URL', cast=DatabaseURL,
                               default='postgresql:///wgsystem?user=wgsystem&host=/db/.s.PGSQL.5432')
DATABASE_TEST_URL = DATABASE_URL.replace(database=f'test_{DATABASE_URL.database}')

### SMTP configuration
SMTP_HOST = smtp_config('SMTP_HOST', default='172.17.0.1')
SMTP_PORT = smtp_config('SMTP_PORT', cast=int, default='25')
