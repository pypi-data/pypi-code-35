"""Common functions and classes for all core classes."""


class Base:
    """Base class for all cleansers"""

    def __init__(self):
        self._text = None

    @property
    def text(self):
        """Property for text that is being cleansed"""
        return self._text

    @text.setter
    def text(self, value):
        """Property setter for text that is being cleansed"""
        self._text = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text!r})"

    def __str__(self):
        return f"{self.text}"
