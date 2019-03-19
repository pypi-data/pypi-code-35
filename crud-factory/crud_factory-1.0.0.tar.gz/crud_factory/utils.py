"""
utils.py

@Author:    Olukunle Ogunmokun
@Date:      10th Dec, 2018
@Time:      3:42 PM

This module contains a number of utility functions useful through the library.
No references are made to specific models or resources. As a result, they are useful with or
without the application context.
"""

import re
import json
from unicodedata import normalize
from datetime import datetime, date, timedelta
from email.utils import formatdate
from calendar import timegm

_slugify_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


class DateJSONEncoder(json.JSONEncoder):
    """ JSON Encoder class to support date and time encoding """

    def default(self, obj):
        if isinstance(obj, (list, tuple)):
            print("Tuple/List", obj)
        if isinstance(obj, datetime):
            return formatdate(timegm(obj.utctimetuple()), usegmt=True)

        if isinstance(obj, date):
            _obj = datetime.combine(obj, datetime.min.time())
            return formatdate(timegm(_obj.utctimetuple()), usegmt=True)

        return json.JSONEncoder.default(self, obj)


class Struct(dict):
    """
    Example:
    m = Struct({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Struct, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Struct, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Struct, self).__delitem__(key)
        del self.__dict__[key]


def expand_errors(data):
    """ Cleans up the error data of forms to enable proper json serialization """
    res = {}
    for k, v in data.items():
        tmp = []
        for x in v:
            tmp.append(str(x))
        res[k] = tmp

    return res


def slugify(text, delim=u'-'):
    """
    Generates an ASCII-only slug.

    :param text: The string/text to be slugified
    :param: delim: the separator between words.

    :returns: slugified text
    :rtype: unicode
    """

    result = []
    for word in _slugify_punct_re.split(text.lower()):
        # ensured the unicode(word) because str broke the code
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word.decode())
    return delim.join(result)


