# coding=utf-8

"""
The By implementation.
"""

class By(object):
    """
    Set of supported locator strategies.
    """

    ID = "id"
    NAME = "name"
    XPATH = "xpath"
    CLASS_NAME = "class name"
    ANDROID_UIAUTOMATOR = '-android uiautomator'
    ACCESSIBILITY_ID = 'accessibility id'
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"

    
    @classmethod
    def is_valid(cls, by):
        for attr in dir(cls):
            if by == getattr(cls, attr):
                return True
        return False