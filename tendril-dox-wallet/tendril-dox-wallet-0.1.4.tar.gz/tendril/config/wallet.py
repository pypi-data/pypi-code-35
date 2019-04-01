

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_wallet = [
    ConfigOption(
        'DOCUMENT_WALLET_ROOT',
        "os.path.join(INSTANCE_ROOT, 'wallet')",
        "Folder for the document wallet filesystem"
    ),
    ConfigOption(
        'DOCUMENT_WALLET',
        "{}",
        "Dictionary containing keys and filenames of the documents "
        "in the wallet"
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_wallet,
                          doc="Document Wallet Configuration")
