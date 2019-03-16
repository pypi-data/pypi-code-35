"""
utils.py

@Author: Olukunle Ogunmokun
@github: https://github.com/kunsam002
@username: Kunsam002
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
import phonenumbers
from unidecode import unidecode
import hashlib
import string
import time
import random

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
    :rtype: str
    """

    result = []
    for word in _slugify_punct_re.split(text.lower()):
        # ensured the str(word) because str broke the code
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word.decode())
    return delim.join(result)


def normalize_text(text):
    """
    Generates an ASCII-only text
    :rtype: str
    """
    if text:
        result = []
        for word in text:
            # ensured the str(word) because str broke the code
            word = re.sub(r'[^\x00-\x7f]', r'', word)
            word = normalize('NFKD', str(word)).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return str(''.join(result))


def clean_ascii(raw):
    """
    Removes ascii characters from the data sent

    :param raw: data to be cleaned (dict)

    returns: cleaned data
    rtype: string
    """
    if type(raw) in [str, list, unicode]:
        clean = filter(lambda x: x in string.printable, raw)
        if len(clean) > 0:
            clean = clean.replace("&", " And ").replace("'s", "").replace("----", "-").replace("---", "-").replace("--",
                                                                                                                   "-").replace(
                "/", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("\\", "").replace(
                "%", "").replace("!", "").replace("__", "-").replace("'", "").replace('"', "")
            clean.encode('ascii', errors='ignore')
    else:
        clean = raw

    return clean


def clean_kwargs(ignored_keys, data):
    """
    Removes the ignored_keys from the data sent

    :param ignored_keys: keys to remove from the data (list or tuple)
    :param data: data to be cleaned (dict)

    returns: cleaned data
    rtype: dict
    """

    for key in ignored_keys:
        data.pop(key, None)

    return data


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it

    :param obj: Object to be populated
    :param data: The data to populate it with (dict)

    :returns: obj populated with data
    :rtype: obj.__class__

    """
    for name, value in data.items():
        if hasattr(obj, name):
            setattr(obj, name, value)

    return obj


def remove_invalid_attributes(obj, data):
    """ remove the attributes of a dictionary that do not belong in an object """
    _data = {}
    for name, value in data.items():
        if hasattr(obj, name):
            _data[name] = value

    return _data


def validate_data_keys(data, keys):
    """
    Check the data dictionary that all the keys are present within it
    """
    for k in keys:
        if not data.has_key(k):
            raise Exception("Invalid data. All required parameters need to be present. Missing Key: [%s]" % k)

    return data


def generate_args_from_keys(data, keys):
    """
    Build an args list from the data parameters passed in.
    This list is converted to a tuple and sent in. The order of the tuple values will match the order of the keys
    """

    res = []
    for k in keys:
        if not data.has_key(k):
            raise Exception("Invalid data. All required parameters need to be present. Missing Key: [%s]" % k)

        res.append(data.get(k))

    return tuple(res)


def copy_dict(source, dest):
    """
    Populates a destination dictionary with the values from the source

    :param source: source dict to read from
    :param dest: destination dict to write to

    :returns: dest
    :rtype: dict

    """
    for name, value in source.items():
        dest[name] = value
    return dest


def remove_empty_keys(data):
    """ removes None value keys from the list dict """
    res = {}

    for key, value in data.items():
        if value is not None:
            res[key] = value

    return res


def prepare_errors(errors):
    _errors = {}
    for k, v in errors.items():
        _res = [str(z) for z in v]
        _errors[str(k)] = _res

    return _errors


def id_generator(size=10, chars=string.ascii_letters.replace("o", "").replace("O", "") + string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size))


def token_generator(size=8, chars=string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size))


def character_generator(size=8, chars=string.ascii_letters.replace("o", "").replace("O", "")):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size))


def code_generator(ignore_case=True):
    """
    Returns a 16 character unique code that can be used as transaction references or other sorts of unique ids
    """
    _token = character_generator(size=2)  # first 2 characters
    _chars = id_generator(size=2)  # last 2 characters or numbers
    _nums = int(time.time() * 100)  # mid 12 numbers

    _code = "%s%s%s" % (_token, _nums, _chars)

    if ignore_case:
        _code = _code.upper()

    return _code


def short_code_generator(ignore_case=True):
    """
    Returns a 10 character unique code that can be used as transaction references or other sorts of unique ids
    """
    _token = character_generator(size=2)  # first 2 characters
    _chars = id_generator(size=2)  # last 2 characters or numbers
    _nums = int(time.time() * 100)
    str_nums = str(_nums)
    _nums = str_nums[-6:]  # mid 6 numbers

    _code = "%s%s%s" % (_token, _nums, _chars)

    if ignore_case:
        _code = _code.upper()

    return _code


def generate_code(obj_id, length=8):
    """ generate a tracking for a package """
    key = str(obj_id) + str(time.time() * 100)
    return str(int(hashlib.md5(key.encode()).hexdigest()[:6], 16)).zfill(length)


def number_format(value):
    return "{:,.2f}".format(float(value))


def is_list(value):
    return isinstance(value, (list, tuple))


def md5_hash(value):
    """ create the md5 hash of the string value """
    return hashlib.md5(value).hexdigest()


def join_list(value, key):
    """ Iterate through a list and retrieve the keys from it """
    return ", ".join([getattr(x, key, "") for x in value])


def clean_phone(number, code):
    _number = code + str(number)

    return _number


def clean_phone_number(number, code):
    num = []
    chars = ['or', 'and', '/', ',']

    for char in chars:
        if char in number:

            number = number.replace(char, "").strip().split()

            count = 0

            _num = []

            while count < len(number):
                nos = number[count]
                nos = filter(lambda x: x.isdigit(), nos)

                if nos.startswith('234'):
                    nos = nos[3:]

                action = clean_phone(int(nos), code)
                _num.append(action)
                count += 1

            return _num

    number = filter(lambda x: x.isdigit(), number)

    if number.startswith('234'):
        number = number[3:]

    _number = clean_phone(int(number), code)
    num.append(_number)

    return num


def format_phone_numbers(raw_numbers, code):
    """
    Properly formats a list or string of phone numbers into the country code

    :param raw_numbers: Phone number to parse and format
    :param code: country code to utilize
    :return: properly formatted phone number or None
    """

    print("This is raw numbers", raw_numbers)

    # Convert list or tuple to string if passed
    if isinstance(raw_numbers, (list, tuple)):
        raw_numbers = ','.join(raw_numbers)
        raw_numbers = re.sub(r'[^\x00-\x7F]+', ' ', raw_numbers)

    numbers = []
    for n in unidecode(str(raw_numbers)).replace("or", ","). \
            replace("\n", ","). \
            replace(".", ","). \
            replace("and", ","). \
            replace(";", ","). \
            replace("/", ",").split(","):
        if len(n) > 0:
            try:
                _n = phonenumbers.parse(n, code)
                if _n and phonenumbers.is_valid_number(_n):
                    cc = _n.country_code
                    nn = _n.national_number
                    num = str(cc) + str(nn)
                    numbers.append(num)
            except Exception as e:
                print(e)

    return numbers


def build_pagination(page, limit, total):
    """ Generate the paging element of the results
    :rtype : object
    """
    pages = (total / limit) + min(1, total % limit)
    prev = max(1, page - 1) if page > 1 else None
    next = min(pages, page + 1) if page < pages else None

    return locals()


def convert_dict(data, indent=None):
    return json.dumps(data, indent=indent, cls=DateJSONEncoder)


def secured_password(password):
    flag = 0
    while True:
        if (len(password) < 8) or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search(
                "[0-9]", password) or not re.search("[_~!@#$%^&{}:;`*()|/='.,<>?+-]", password) or re.search("\s",
                                                                                                             password):
            flag = -1
            break
        else:
            flag = 0
            print("Valid Password")
            break

    if flag == -1:
        print("Not a Valid Password")
        return False
    else:
        print("Password Valid")
        return True
