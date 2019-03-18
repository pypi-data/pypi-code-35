#coding: utf8
from __future__ import absolute_import
import sys
import os
import hashlib
import re
import uuid


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = (str, bytes)
    unicode = str
else:
    string_types = basestring
    unicode = unicode


def to_bytes(s):
    if not isinstance(s, string_types):
        s = smart_unicode(s)
    if isinstance(s, unicode):
        s = s.encode('utf8')
    else:
        try:
            s = str(s)
        except:
            pass
    return s

ENCODINGS = [
    "utf8",
    "gb18030",
    "big5",
    "latin1",
    "ascii"
]
def to_unicode(s):
    if not isinstance(s, string_types):
        try:
            s = unicode(s)
        except:
            try:
                s = str(s)
            except:
                pass
    if not isinstance(s, unicode):
        for encoding in ENCODINGS:
            try:
                s = unicode(s, encoding)
                return s
            except:
                pass
    return s

smart_unicode = to_unicode
smart_str = to_bytes

def get_md5(content, block_size=0): # 1024*1024 2**20, block_size=1Mb
    content = smart_str(content)
    if not block_size:
        return hashlib.md5(content).hexdigest()
    else:
        md5_obj = hashlib.md5()
        n = len(content)
        for i in range(0, n, block_size):
            md5_obj.update(content[i:i+block_size])
        return md5_obj.hexdigest()

class UnicodeWithAttrs(unicode):
    pass


def is_str(content):
    try:
        str(content)
        return True
    except:
        return False


def unique_list(data):
    # 类似 set 功能，但是保留原来的次序
    new_data = []
    for row in data:
        if row not in new_data:
            new_data.append(row)
    return new_data


def string_to_list(value):
    if not value:
        return []
    if isinstance(value, (str, unicode)) and value:
        if ',' in value:
            ls = value.split(',')
        elif u'，' in value:
            ls = value.split(u'，')
        else:
            ls = value.split(' ')
        ls = [item.strip() for item in ls if item]
        return unique_list(ls)
    elif type(value) in [list, tuple]:
        value = unique_list(value)
        return [smart_unicode(row).strip() for row in value if row]
    else:
        return [smart_str(value)]


def same_slash(filepath):
    filepath = filepath.rstrip('/').replace('\\', '/')
    filepath = smart_unicode(filepath)
    return filepath


def get_relative_path(filepath, root, return_name_if_fail=True):
    # without '/' in head/foot
    filepath = same_slash(filepath)
    root = same_slash(root)
    if filepath and root and filepath.startswith(root+'/'):
        return filepath.replace(root, '').strip('/')
    elif filepath == root:
        return ''
    else:
        if return_name_if_fail:
            return os.path.split(filepath)[-1]
        else:
            return filepath



class LazyDict(dict):
    # 非常有用的一个处理，可以让dict 之类的数据，可以直接调用property 的写法
    def __getitem__(self, item):
        try:
            value = dict.__getitem__(self, item)
        except:
            value = LazyDict()
        return value

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __repr__(self):
        return ''

    def __nonzero__(self):
        return 0


class LazyBool(object):
    # 这样在最终调用的时候，避免有True/False的输出，但是又能作为条件的判断
    def __init__(self, value):
        self.value = value
    def __nonzero__(self):
        if self.value:
            return 1
        else:
            return 0
    def __repr__(self):
        return ''
    def __unicode__(self):
        return ''
    def __str__(self):
        return ''


class ErrorInfo(unicode):
    def __nonzero__(self):
        # 这样判定 if 的时候，始终False
        return 0


def make_content_clean(content):
    content = smart_unicode(content)
    content = content.replace(u'\xa0', u' ')
    content = re.sub('\x07|\x08|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f', '', content)
    return content



def get_uuid():
    return uuid.uuid1().hex


def get_random_html_dom_id():
    return 'd_%s' % get_uuid()