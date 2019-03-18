import logging
from sys import version_info


class PathTruncatingFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', max_name_len=20,
                 strip_py=True):
        """
        Logging Formatter for truncating fields.
        Note: style does not work in Python version < 3.2. This parameter
        is silently ignored.
        See logging.Formatter for more detailed parameter info
        Args:
            fmt: format string
            datefmt: date format
            style: Use a style parameter of '%', '{' or '$' to specify that you
                want to use one of %-formatting, :meth:`str.format` (``{}``)
                formatting or :class:`string.Template` formatting in your
                format string.
            max_name_len: Trim the filename to this length
            strip_py: If true, remove '.py' from filename
        """
        self.max_name_len = max_name_len
        self.strip_py = strip_py
        if version_info.major >= 3:
            super(PathTruncatingFormatter, self).__init__(
                fmt=fmt, datefmt=datefmt, style=style)
        else:
            super(PathTruncatingFormatter, self).__init__(
                fmt=fmt, datefmt=datefmt)

    def format(self, record):
        filename = getattr(record, 'filename')

        if self.strip_py:
            filename = filename.strip('.py')
        if len(filename) > self.max_name_len:
            len0 = self.max_name_len // 2
            len1 = self.max_name_len - (len0 + 1)
            filename = '{}~{}'.format(filename[:len0], filename[-len1:])
        setattr(record, 'filename', filename)
        return super(PathTruncatingFormatter, self).format(record)
