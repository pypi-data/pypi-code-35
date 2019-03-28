"""Common generic methods for cleaning text."""
import re
from cleanser.core import Base

RE_WHITESPACE = re.compile(r"\s+")
RE_EMOJI = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)
URL_REGEX = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


class Generic(Base):
    """Common generic methods for cleaning text."""

    def whitespaces(self):
        """Removes extra spaces, tabs, and newlines from text."""
        self.text = RE_WHITESPACE.sub(" ", self.text).strip()
        return self

    def emojis(self):
        """Removes emojis from text."""
        self.text = RE_EMOJI.sub("", self.text)
        return self

    def urls(self):
        """Removes urls from text."""
        self.text = URL_REGEX.sub("", self.text)
        return self
