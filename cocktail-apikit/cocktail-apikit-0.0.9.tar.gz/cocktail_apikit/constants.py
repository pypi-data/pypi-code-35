"""
Constants used in api project
"""
from marshmallow.fields import (
    Raw, Nested, Dict, List, String, UUID, Number, Integer, Decimal, Boolean, FormattedString,
    Float, DateTime, LocalDateTime, Time, Date, TimeDelta, Url, URL, Email, Str, Bool, Int, Constant
)

############################################################
# Marshmallow's field categories
############################################################
MARSHMALLOW_LIST_FIELDS = (List,)
MARSHMALLOW_NESTED_FIELDS = (Nested,)
MARSHMALLOW_DICT_FIELDS = (Dict,)
MARSHMALLOW_SCALAR_FIELDS = (
    Raw, Constant,
    UUID, String, Str, FormattedString, str,
    Number, Integer, Int, int, Decimal,
    Boolean, Bool, bool,
    Float, float,
    Date, DateTime, LocalDateTime, Time, TimeDelta,
    Email, URL, Url,
    # Function, Method
)

############################################################
# Mongo operator customie mapping
############################################################
MONGO_LOOKUPS_MAPPINGS = {
    'lt': '$lt',
    'lte': '$lte',
    'gt': '$gt',
    'gte': '$gte',
    'in': '$in',
    'regex': '$regex',
    'exists': '$exists',
    'all': '$all',
    'size': '$size',
    'type': '$type',
    'text': '$text',
    'where': '$where',

    # 'elemmatch': '$elemmatch',

    # TODO: there are more other operaters need to introduce here
    # ...
}

############################################################
# Separator which used to separate request's field & operator
############################################################
REQUEST_LOOKUP_MARK = '__'

############################################################
# Mark to indicate sort a field by desc order
############################################################
REQUEST_DESC_SORT_MARK = '-'

############################################################
# Request's query string's constants
############################################################
SORT_KEY = 'sort'
PAGE_KEY = 'page'
LIMIT_KEY = 'limit'

############################################################
# Database constants
############################################################
RECORD_ACTIVE_FLAG_FIELD = '_enabled'
MONGO_ID_FIELD_NAME = '_id'

############################################################
# HTTP messages
############################################################
HTTP_OK = 'OK'
HTTP_DELETE_OK = 'Delete Success'
HTTP_UPDATE_OK = 'Update Success'
