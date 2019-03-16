import feedparser

from picot.entry import Entry


def _ok_to_all_filter(x):
    """This is the default filter function."""

    return True


class Feed(object):
    """This class encapsulates the feed providing filtering and
    formatting hooks.
    This provides an iterator on the selected entries.

    Example:
        feed = Feed(url)
        feed_filtered = Feed(
            url,
            filter_func=lambda x: x['title'].startswith('Episode')
        )
        feed_formatted = Feed(
            url,
            format_func=lambda x: '{} {}'.format(x['title'], x['link'])
        )
    """

    def __init__(self, url, filter_func=None, format_func=None):
        """This initializes the Feed object with corresponding filter
        and format functions.
        """
        if filter_func is None:
            filter_func = _ok_to_all_filter
        self.filter_func = filter_func
        self.format_func = format_func
        self._feed = feedparser.parse(url)
        self._entries = None

    def _update_entries(self):
        """This updates the entries according to the filter
        function.
        """
        if self._entries is None:
            self._entries = [Entry(entry, format_func=self.format_func)
                             for entry in self._feed.entries if
                             self.filter_func(entry)]

    def __iter__(self):
        """This makes the class an iterator on the selected
        entries, after applying the filter.
        """
        self._update_entries()
        return iter(self._entries)

    def __len__(self):
        """This calculates the amount of selected entries after
        applying the filter."""
        self._update_entries()
        return len(self._entries)

    def __repr__(self):
        """This generates a representation of the feed."""
        return "{} ({})".format(
            self._feed.feed.title,
            self._feed.feed.link
        )
