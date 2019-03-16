class Entry(dict):
    """This class encapsulates a feed's entry providing formatting.

    Example:
        entry = Entry(raw_entry)
        formatted_entry = Entry(
            raw_entry,
            format_func=lambda x: '{}'.format(x['title']
        )
    """

    def __init__(self, *args, **kwargs):
        """This initializes the the Entry object with corresponding
        format function.
        """
        super(Entry, self).__init__(args[0])
        self._format_func = super(Entry, self).__repr__
        if 'format_func' in kwargs:
            self._format_func = kwargs['format_func']

    def __repr__(self):
        """This generates a representation of the entry."""
        if self._format_func is None:
            return super().__repr__()
        else:
            return self._format_func(self)
