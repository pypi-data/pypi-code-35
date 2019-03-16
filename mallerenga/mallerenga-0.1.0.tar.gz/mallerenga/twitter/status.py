class Status(object):
    """This encapsulates the Twitter reply to a tweet."""

    def __init__(self, status):
        """This initializes the object storing metadata."""
        self._status = status

    @property
    def id(self):
        return self._status.id

    @property
    def username(self):
        """This formats the username."""
        return '@{}'.format(self._status.user.screen_name)

    @property
    def link(self):
        """This formats the URL to the link for the tweet."""
        return 'https://twitter.com/{0.user.screen_name}/status/{0.id}'.format(
            self._status,
        )

    @property
    def text(self):
        return self._status.text

    @property
    def time(self):
        """This provides access to creation time."""
        return self._status.created_at

    def __repr__(self):
        """This returns a representation of the status object."""
        return '{0.time} {0.id} {0.username} {0.text}'.format(self)
