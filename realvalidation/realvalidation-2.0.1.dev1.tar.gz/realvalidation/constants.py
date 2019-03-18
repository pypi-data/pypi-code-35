from pkg_resources import get_distribution, DistributionNotFound

VERSION = None

try:
    VERSION = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    VERSION = "ERROR"

DESCRIPTION = "RealValidation v{}".format(VERSION)

MOCK_DNC_URL = 'https://realvalidation-dnc-mock.herokuapp.com/validate'
PROD_DNC_URL = 'https://api.realvalidation.com/rpvWebService/DNCLookup.php'

PHONE_COLUMN_REGEX = r'^phone$'
PHONE_DIGIT_REGEX = r'^\d{10}$'

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'
