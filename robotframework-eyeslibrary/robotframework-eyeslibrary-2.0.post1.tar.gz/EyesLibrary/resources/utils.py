import httplib
from applitools.core import logger, StdoutLogger
from applitools.eyes import MatchLevel
from applitools.core import EyesIllegalArgument
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException



def get_match_level(matchlevel):

    selected_match_level = None

    if matchlevel.upper() == "STRICT":
        selected_match_level = MatchLevel.STRICT
    elif matchlevel.upper() == "CONTENT":
        selected_match_level = MatchLevel.CONTENT
    elif matchlevel.upper() == "LAYOUT":
        selected_match_level = MatchLevel.LAYOUT
    elif matchlevel.upper() == "EXACT":
        selected_match_level = MatchLevel.EXACT
    else:
        raise EyesIllegalArgument(
            "Please select a valid match level: Strict, Content, Layout, Exact"
        )

    return selected_match_level


def get_selector_strategy(selector):

    selected_strategy = None

    if selector.upper() == "CSS SELECTOR":
        selected_strategy = By.CSS_SELECTOR
    elif selector.upper() == "XPATH":
        selected_strategy = By.XPATH
    elif selector.upper() == "ID":
        selected_strategy = By.ID
    elif selector.upper() == "LINK TEXT":
        selected_strategy = By.LINK_TEXT
    elif selector.upper() == "PARTIAL LINK TEXT":
        selected_strategy = By.PARTIAL_LINK_TEXT
    elif selector.upper() == "NAME":
        selected_strategy = By.NAME
    elif selector.upper() == "TAG NAME":
        selected_strategy = By.TAG_NAME
    elif selector.upper() == "CLASS NAME":
        selected_strategy = By.CLASS_NAME
    else:
        raise InvalidElementStateException(
            "Please select a valid selector: CSS SELECTOR, XPATH, ID, LINK TEXT, PARTIAL LINK TEXT, NAME, TAG NAME, CLASS NAME"
        )

    return selected_strategy


def manage_logging(enable_eyes_log, enable_http_debug_log):
    
    if enable_eyes_log is True:
        logger.set_logger(StdoutLogger())
        logger.open_()
    if enable_http_debug_log is True:
        httplib.HTTPConnection.debuglevel = 1
