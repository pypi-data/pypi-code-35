import logging


def ips_logger() -> logging.Logger:
    """
    Author        : Elinor Thorne
    Date          : 5 Jan 2018
    Purpose       : Sets up and returns database logger object
    Parameters    : None
    Returns       : Database logger object
    Requirements  : None
    Dependencies  : social_surveys.setup_logging
    """

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger()

log = ips_logger()

