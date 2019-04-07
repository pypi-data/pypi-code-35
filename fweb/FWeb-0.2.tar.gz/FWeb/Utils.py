import os
import platform
import urllib

PATH_SEP = "/" if platform.system() == "Linux" else "\\"


def is_file_exist(path):
    return os.path.exists(path) and os.path.isfile(path)


def parse_qs(data, line_split="&", equal_split="=", decode=True):
    res = {}
    for i in data.split(line_split):
        if not i: continue
        if equal_split in i:
            k, v = i[:i.find(equal_split)], i[i.find(equal_split) + len(equal_split):]
        else:
            k, v = i, ""
        if decode: res[k] = url_decode(v)
    return res

def url_decode(code):
    code = code.replace("+", " ")
    return urllib.parse.unquote(code)