import sys

if sys.version < '3':
    str_types = (str, unicode)  # noqa F821 undefined name 'unicode'

else:
    str_types = str
