#coding: utf8
from __future__ import absolute_import
from dateutil.parser import parse as parse_date
import datetime, re, unidecode, time
from collections import OrderedDict
from farbox_lite.utils import smart_unicode, smart_str, LazyDict, get_md5, UnicodeWithAttrs
from farbox_lite.utils.functional import curry


def is_public(value):
    if value in [True, 'public', 'open', 'on', 'published', 'true', 'yes']:
        return True
    else:
        return False

is_on = is_public

def is_closed(value):
    if value in ['no', 'false', False, 'off', 'close']:
        return True
    else:
        return False


def dict_parts(dt, parts):
    return {part: dt.get(part) for part in parts}


def list_to_dict(keys, values):
    data = {}
    for i, value in enumerate(values):
        if isinstance(value, (str, unicode)):
            value = value.strip()
        try:
            key = keys[i]
            data[key] = value
        except:
            pass
    for key in keys:
        if key not in data:
            data[key] = None
    return data


def get_value_from_data(data, attr, default=None):
    if isinstance(data, dict) and attr in data:
        # dict 类型，直接返回value，attr本身可能包含 .
        return data[attr]
    try:
        attrs = attr.split('.')[:25] # 最多允许25个遍历
        for attr in attrs:

            # 因为系统默认是建立在 path 上的，所以字符串的 parent 会寻找 parent
            if attr == 'parent_path' and isinstance(data, (str, unicode)):
                if '/' not in data:
                    return ''
                else:
                    return data.rsplit('/', 1)[0]

            # 最后一个dt是真实的value
            if type(data) in [dict, OrderedDict]:
                data = data.get(attr, None)
            else:
                try:
                    data = getattr(data, attr, None)
                except: # jinja 中的 Undefined 会触发错误
                    return data
            if data is None or isinstance(data, LazyDict):  # 到底了
                if default is not None:
                    return default
                else:
                    return None
    except RuntimeError: # 一般是在外部调用g/request的时候会遇到
        return None
    return data

def set_attr_to_obj(obj, attr, value):
    try:
        setattr(obj, attr, value)
    except RuntimeError: # 一般是在外部调用g/request的时候会遇到
        pass


def merge_datas(*args):
    # 最后一个字典的值最优先，逻辑为依次覆盖
    data = dict()
    for dt in args:
        if type(dt) != dict: # 非字典
            data.update(getattr(data, '__dict__', {}))
        else:  # 字典
            data.update(dt)
    return data


def clone_field_from_other_dict(current, other, fields=()):
    # 一个dict，从另外的dict，按照指定的fields进行value clone
    for field in fields:
        if field in other:
            value_on_other = other.get(field)
            current[field] = value_on_other
    return current


class dict_to_obj(object):
    def __init__(self, dt):
        for a, b in dt.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [self.__class__(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, self.__class__(b) if isinstance(b, dict) else b)


def to_number(value, default_if_fail=None, max_value=None, min_value=None, number_type_func=None):
    if isinstance(value, (str, unicode)):
        value = value.strip()
    if not value and type(value)!=int:
        return default_if_fail
    try:
        value = float(value)
        if number_type_func:
            value = number_type_func(value)
    except:
        value = default_if_fail
    if max_value is not None and value > max_value:
        value = max_value
    if min_value is not None and value < min_value:
        value = min_value
    return value


def to_float(value, default_if_fail=None, max_value=None, min_value=None):
    if isinstance(value, (str, unicode))  and '/' in value and value.count('/')==1: # 分数
        k1, k2 = value.split('/', 1)
        k1 = to_float(k1)
        k2 = to_float(k2)
        if k1 and k2:
            value = k1/k2
    return to_number(value, default_if_fail=default_if_fail, max_value=max_value, min_value=min_value)


to_int = curry(to_number, number_type_func=int)



def string_to_int(value):
    if not value:
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, (str, unicode)): # 提取字符串中的整数部分，作为value
        re_s = re.search('\d+', value)
        if re_s:
            int_value = re_s.group()
            return to_int(int_value)
    # at last
    return to_int(value)


def is_str(text, includes=''):
    if not isinstance(text, (str, unicode)):
        return False
    text = text.strip()
    if includes:
        for s in includes: text=text.replace(s, '')
    if not text:
        return False
    return bool(re.match(r'[a-z0-9_\-]+$', text, flags=re.I))


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


def simple_kv_dict(data_list):
    # 将一个字符串的 list，内用空格或者冒号形成的 kv 结构转为 dict 模式
    if isinstance(data_list, (str, unicode)):
        data_list = string_to_list(data_list)
    if not isinstance(data_list, (list, tuple)):
        return data_list # ignore
    result_dict = {}
    for row in data_list:
        if not isinstance(row, (str, unicode)):
            continue
        parts = re.split(u'\uff1a|:', row, 1)
        if len(parts) == 2:
            k, v = parts
            result_dict[k.strip()] = v.strip()
        elif len(parts) == 1 and ' ' in row: # 尝试用空格分割
            parts = row.split(' ', 1)
            k, v = parts
            result_dict[k.strip()] = v.strip()
    return result_dict




def slugify(value, must_lower=True, auto=False):
    # auto=True 表示是自动生成的
    value= smart_unicode(value)
    value = unidecode.unidecode(value).strip()
    if must_lower:
        value = value.lower()
    value = re.sub(r'[ &~,"\':*+?#{}()<>\[\]]', '-', value).strip('-')  # 去掉非法的url字符
    value = re.sub(r'-+', '-', value)  # 替换连续的 --的或者-/
    value = value.replace('-/', '/')
    if auto: # 去掉可能的序号, 这样自动生成的 url 美观一点
        value = re.sub(r'^\d{1,2}(\.\d+)? ', '', value).strip() or value
        value = value.strip('-_')
    value = value.strip('/') # 头尾不能包含 /
    return value


def to_date(value):
    if not value:
        return None
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(getattr(value, 'core', None), datetime.datetime): # 被Date给wrap了
        return getattr(value, 'core', None)
    else:
        try:
            return parse_date(value)
        except:
            return None


def auto_type(value):
    # 自动类型，主要是 str 类的转为 number 的可能
    if not isinstance(value, (str, unicode)):
        return value
    value = value.strip()
    if re.match('^\d+$', value):
        return int(value)
    if re.match('^\d+\.(\d+)?$', value):
        return float(value)
    if re.match('^\d+/\d+$', value): # 分数
        new_value = to_float(value)
        if new_value:
            return new_value
    if value in ['True', 'true']:
        return True
    if value in ['False', 'false']:
        return False
    # at last
    return value


def re_sub(pattern, repl, string, count=0, flags=0):
    # 避免 re 的 sub 内如果 content 有 #/g 这种特定的非安全写法
    founds = re.findall(pattern, string, flags=flags)
    if count:
        founds = founds[:count]
    for found in founds:
        string = string.replace(found, repl, 1)
    return string


def simple_yaml_str(data, full=False):
    to_return = ''
    for key, value in data.items():
        to_return += '%s: %s\n' % (key, value)
    if full:
        to_return = '---\n%s---\n' % to_return
    return to_return


def count_words(content):
    # http://www.khngai.com/chinese/charmap/tbluni.php?page=0
        # 4e00 - 9fff是中文字符集的头尾 # 19968 - 40959
        # 3000 - 4db0 日文   # 3000-19888
        # 1100–11FF  # 韩文
        # 44032 - 55203 3130-12687 43360-43391  55216-55295
        # 0.5s 大概可以处理 176w的unicode
        # 2k字算的话，大概0.0005s，应该不会有性能问题
    content = smart_unicode(content)
    total_words = len(re.findall(ur'[\w\-_/]+|[\u1100-\ufde8]', content)) # 直接 1100 - 65000
    return total_words


def cut_content_by_words(content, max_words, mark=u'...'):
    if not isinstance(max_words, int):
        return content
    if max_words < 1:
        return content
    if max_words > 2000:
        max_words = 2000 # 最大不能超过这个，不然性能问题
    content = smart_unicode(content)
    iter_found = re.finditer(ur'[\w\-_/]+|[\u1100-\ufde8]', content)
    n = 0
    end = 0
    for i in iter_found:
        end = i.end()
        n += 1
        if n >= max_words:
            break
    if end:
        new_content = content[:end]
        if len(content) > end:
            mark = smart_unicode(mark)
            new_content += mark
            new_content = UnicodeWithAttrs(new_content)
            new_content.has_more = True
        return new_content
    else:
        return content



def str_equal(s1, s2, lower=False):
    if not s1 and not s2:  # 都为空的时候，返回False
        return False
    s1 = smart_unicode(s1)
    s2 = smart_unicode(s2)
    if lower:
        return s1.lower() == s2.lower()
    else:
        return s1 == s2


def bytes2human(num):
    if isinstance(num, (str, unicode)):
        return num
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def seconds2human(seconds):
    mins = int(seconds/60)
    seconds_left = int(seconds - mins*60)
    return '%s:%02d' % (mins, seconds_left)


# 将一个整数，压码为字符串
def encode_int_to_str(n):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    alphabet_length = len(alphabet)
    encoded = ''
    while n > 0:
        n, r = divmod(n, alphabet_length)
        encoded = alphabet[r]+encoded
    return encoded


def decode_str_to_int(s):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    alphabet_length = len(alphabet)
    s_length = len(s)
    d = dict((ch, i) for (i, ch) in enumerate(alphabet))
    n = sum(d[ch] * alphabet_length**(s_length-i-1) for (i,ch) in enumerate(s))
    return n


# 提取附属星系， 比如 hello (x=y, k=v) 其中括号内的内容会形成 kv 结构的字典, 仅限单行
def extract_extra_info(line):
    line = line.replace('&quot;', '"').replace('&apos;', "'")
    line = line.replace('<em>', '_').replace('</em>', '_') # 跟Markdown解析后的HTML混淆了，转义回来
    extra_info ={}
    if isinstance(line, (str, unicode)) and '\n' not in line and '{' in line and line.endswith('}'): # 对 {}的兼容
        # 因为要提取的内部，是不能包含 () 的， 所以用 {} 进行替换； 但前提是 尾部由 } 结尾，以免造成不必要的处理
        line = line.replace('{', '(').replace('}', ')')
    if isinstance(line, (str, unicode)) and '\n' not in line and '(' in line and line.endswith(')'):
        if ',' not in line and '&' in line:
            line = line.replace('&', ',')

        c = re.search(r'(.*?)\((.*?)\)$', line)
        if c:
            new_line, extra_info_s = c.groups()
            line = new_line.strip()
            # lazy_list(type=dom_list, form_keys=[key, value], title='Content')  -> 这个分割比较困难
            if ', ' in extra_info_s: # 为了允许 , 也能用，就要确保field之间的声明用 “, ”，确保后续的空格
                parts = extra_info_s.split(', ')
            else:
                parts = extra_info_s.split(',')
            for extra_info_part in parts:
                if '=' not in extra_info_part:
                    continue
                k, v = extra_info_part.split('=', 1)
                k = k.strip()
                v = v.strip('\'"').strip()
                if re.match('\d+$', v):
                    v = int(v)
                elif re.match(r'\d+\.\d+$', v):
                    v = float(v)
                elif (v.startswith('[') and v.endswith(']')) or (v.startswith('(') and v.endswith(')')): # list
                    v = v[1:-1]
                    v = string_to_list(v)
                elif v.lower() in ['true', 'yes']:
                    v = True
                elif v.lower() in ['false', 'no']:
                    v = False
                extra_info[k] = v
    return line, extra_info



def make_list_small(ls, keys):
    result = []
    for row in ls:
        if not isinstance(row, dict):
            result.append(row)
        else:
            new_value = {key: row.get(key) for key in keys}
            result.append(new_value)
    return result



def all_has(doc, fields):
    if not doc:
        return False
    for field in fields:
        if not doc.get(field):
            return False
    return True



class cached(object):
    """
    @cached
    def xxxx():
        xxxx

    @cached(60, cache_key=None or other...)
    def xxx():
        xxxxxxx
    """
    def __init__(self, first_arg=None, cache_key=None):
        self.cached_function_responses = {}
        self.direct_func = None
        self.default_cache_key = cache_key

        if hasattr(first_arg, '__call__'):
            # 直接调用了这是
            # @cached
            # def xxxx(): .....
            self.max_age = 0
            self.direct_func = first_arg
        else:
            # 指定了缓存的时间
            # @cached(60)
            # def xxxx(): .......
            if not isinstance(first_arg, int):
                self.max_age = 0
            else:
                self.max_age = first_arg or 0

    def __call__(self, *args, **kwargs):
        def _func(*func_args, **func_kwargs):
            now = time.time()

            if self.direct_func:
                func = self.direct_func
            else:
                func = args[0]

            # 计算缓存的key值，根据传入的函数参数不同可以推断，如果没有函数传入，则相当于func本身的id（整数）
            # func_id 是作为cache_key的base
            if self.default_cache_key:
                base_cache_key = self.default_cache_key
            else:
                base_cache_key = id(func)
            if func_args or func_kwargs:
                # 可能第一个变量传入的是 self 这种实例对象
                func_args_s_list = [] # 形成缓存key用的一个list
                for func_arg in func_args:
                    if isinstance(func_arg, dict) and func_arg.get('_id'):
                        func_args_s_list.append(smart_unicode(func_arg.get('_id')))
                    elif not isinstance(func_arg, (str, unicode, dict, tuple, list, bool, int, float)):
                        func_args_s_list.append(str(id(func_arg)))
                    else:
                        func_args_s_list.append(smart_unicode(func_arg))
                var_key = smart_unicode('-'.join(func_args_s_list)) + smart_unicode(func_kwargs)
                var_md5 = get_md5(var_key)
                cache_key = '%s-%s' % (base_cache_key, var_md5)
            else:
                cache_key = base_cache_key

            if cache_key in self.cached_function_responses:
                cached_obj = self.cached_function_responses[cache_key]
                cached_data = cached_obj['data']
                cached_time = cached_obj['cache_time']
                if not self.max_age: # 相当于直接缓存，没有过期时间
                    return cached_data
                else: # 查看是否过期
                    if now - cached_time < self.max_age:
                        return cached_data
            result = func(*func_args, **func_kwargs)
            self.cached_function_responses[cache_key] = dict(data=result, cache_time=now)
            return result

        if self.direct_func:
            return _func(*args, **kwargs)
        else:
            return _func


def split_list(ls, size_per_part):
    for i in range(0, len(ls), size_per_part):
        yield ls[i:i + size_per_part]


def auto_choose(key, choices):
    # 一个key过来，会指定一个choice，而不是随机的; choices 本身要是已经sort的list。
    if not choices:
        return # ignore, return None
    if len(choices) == 1:
        return choices[0]
    if isinstance(key, dict) and '_id' in key:
        # 传入的key可能是一个数据库对象，以其_id作为key
        key = key['_id']
    key = get_md5(key)
    number = int(''.join([str(ord(s)) for s in key[:5]]))
    key_number = number % len(choices)
    return choices[key_number]