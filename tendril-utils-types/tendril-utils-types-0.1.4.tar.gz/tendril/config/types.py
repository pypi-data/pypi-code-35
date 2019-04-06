

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = []


config_elements_currency = [
    ConfigOption(
        'BASE_CURRENCY',
        "INR",
        "The code for the base currency."
    ),
    ConfigOption(
        'BASE_CURRENCY_SYMBOL',
        "INR ",
        "The symbol for the base currency."
    ),
    ConfigOption(
        'BASE_CURRENCY_NAME',
        "Indian Rupees",
        "The name of the base currency when used with num2words.",
    ),
    ConfigOption(
        'BASE_CURRENCY_LANG',
        "en_IN",
        "The language to use for the base currency when used with num2words."
    ),
    ConfigOption(
        "FIXER_IO_API_KEY",
        "",
        "API Key to use with fixer.io for currency rates."
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_currency,
                          doc="Native Currency and Exchange Rate API Configuration")
