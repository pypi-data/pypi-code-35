"""Utilities specifically for cleaning text from Reddit."""
import re
from cleanser.core import Base

REDDIT_MENTIONS = re.compile(r"/?u/\S+")
REDDIT_SUBREDDITS = re.compile(r"/?r/\S+")
REDDIT_QUOTES = re.compile(r"^\>.*$", flags=re.MULTILINE)
REDDIT_BOLD_ITALICS = re.compile(r"\*+")
REDDIT_CODE = re.compile(r"\`")
REDDIT_SUPERSCRIPT = re.compile(r"\^")
REDDIT_HEADERS = re.compile(r"\#+")
REDDIT_STRIKETHROUGH = re.compile(r"~{2}.*~{2}")
REDDIT_SPOILERS = re.compile(r">!|!<")
# REDDIT_LINKS = re.compile(r"\[.*\]\(.*\)")


class Reddit(Base):
    """Common methods for cleaning text from Reddit."""

    def reddit_mentions(self):
        """Removes reddit user mentions from text."""
        self.text = REDDIT_MENTIONS.sub("", self.text)
        return self

    def reddit_subreddits(self):
        """Removes reddit subreddit mentions from text."""
        self.text = REDDIT_SUBREDDITS.sub("", self.text)
        return self

    def reddit_quotes(self):
        """Removes reddit quotes from text."""
        self.text = REDDIT_QUOTES.sub("", self.text)
        return self

    def reddit_bold_italics(self):
        """Removes reddit bolding and italics from text."""
        self.text = REDDIT_BOLD_ITALICS.sub("", self.text)
        return self

    def reddit_code(self):
        """Removes reddit code formatting from text."""
        self.text = REDDIT_CODE.sub("", self.text)
        return self

    def reddit_superscript(self):
        """Removes reddit superscript formatting from text."""
        self.text = REDDIT_SUPERSCRIPT.sub("", self.text)
        return self

    def reddit_headers(self):
        """Removes reddit header formatting from text."""
        self.text = REDDIT_HEADERS.sub("", self.text)
        return self

    def reddit_strikethrough(self):
        """Removes reddit strikethrough formatted text."""
        self.text = REDDIT_STRIKETHROUGH.sub("", self.text)
        return self

    def reddit_spoilers(self):
        """Removes reddit spoiler formatting from text."""
        self.text = REDDIT_SPOILERS.sub("", self.text)
        return self
