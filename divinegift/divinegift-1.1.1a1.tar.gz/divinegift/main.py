from divinegift.logger import log_info, log_err, log_warning
from divinegift.cipher import caesar_code, get_cipher, read_key, encrypt_str, decrypt_str, get_key, write_key
#########################################################################
import json
import sys
from datetime import datetime
import re
import os
import math
from collections import defaultdict

datetime_regex = r'20\d{2}(-|\/)((0[1-9])|(1[0-2]))(-|\/)((0[1-9])|([1-2][0-9])|(3[0-1]))(T|\s)(([0-1][0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9])'


class Settings:
    def __init__(self):
        self.settings = {}
        self.cipher_key = None

    def get_settings(self):
        return self.settings

    def set_settings(self, json_str: object):
        self.settings = json_str

    def parse_settings(self, file: str = './settings.conf', encoding: str = 'utf-8', log_changes: bool = True):
        """
        Parse settings from file
        :param file: Filename with settings
        :param encoding: Encoding
        :return: None
        """
        json_data = parse_json(file, encoding=encoding)

        if log_changes and json_data:
            dict_c = dict_compare(self.settings, json_data)
            added, removed, modified, same = dict_c.values()
            if len(added) > 0:
                for r in list(added):
                    log_warning('Added {}: {}'.format(r, json_data.get(r)))
            if len(removed) > 0:
                for r in list(removed):
                    log_warning('Removed {}: {}'.format(r, self.settings.get(r)))
            if len(modified) > 0:
                for r in list(modified):
                    log_warning('Modified {}: {} -> {}'.format(r, modified.get(r)[0], modified.get(r)[1]))
        elif log_changes and not json_data:
            raise Exception('Settings not parsed. Is there any data?')

        self.set_settings(json_data)

    def initialize_cipher(self, ck_fname: str = 'key.ck'):
        self.cipher_key = get_key()
        write_key(ck_fname, self.cipher_key)

    def encrypt_password(self, conn_name: str, ck_fname: str = 'key.ck'):
        if not self.cipher_key:
            self.cipher_key = read_key(ck_fname)
            if not self.cipher_key:
                self.initialize_cipher()
        cipher = get_cipher(self.cipher_key)
        self.settings[conn_name]['db_pass'] = encrypt_str(self.settings[conn_name]['db_pass'], cipher)

    def decrypt_password(self, conn_name: str, ck_fname: str = 'key.ck'):
        if not self.cipher_key:
            self.cipher_key = read_key(ck_fname)
        cipher = get_cipher(self.cipher_key)
        self.settings[conn_name]['db_pass'] = decrypt_str(self.settings[conn_name]['db_pass'], cipher)

    def encode_password(self, conn_name: str):
        settings = self.get_settings().copy()
        settings[conn_name]['db_pass'] = encode_password(settings[conn_name]['db_pass'])
        self.set_settings(settings)

    def decode_password(self, conn_name: str):
        settings = self.get_settings().copy()
        settings[conn_name]['db_pass'] = decode_password(settings[conn_name]['db_pass'])
        self.set_settings(settings)

    def save_settings(self, file_name: str = './settings.conf'):
        create_json(file_name, self.get_settings())


def dict_compare(d1: dict, d2: dict):
    """
    Compare 2 dict
    :param d1: First dict to compare
    :param d2: Second dict
    :return: Dict with results of comparing
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])

    result = {'added': list(added), 'removed': list(removed), 'modified': modified, 'same': list(same)}
    return result


def get_args():
    """
    Get dict of args by pairs (e.g. --log_level 'INFO')
    :return: dict of args
    """
    args = sys.argv
    args_d = {}
    for i, arg in enumerate(args):
        if i == 0:
            args_d['name'] = arg
            continue
        if arg.startswith('-') or arg.startswith('--'):
            if i != len(args) - 1:
                if not args[i + 1].startswith('-') or not args[i + 1].startswith('--'):
                    args_d[arg] = args[i + 1]
                else:
                    args_d[arg] = True
            else:
                args_d[arg] = True
        else:
            continue

    return args_d


def get_log_param(args: dict):
    """
    Get log_level and log_name from args
    :param args: dict of args from get_args()
    :return: log_level and log_name for set_loglevel()
    """
    log_level = None
    log_name = None
    log_dir = None
    for key in args.keys():
        if key in ['--log_level', '-ll']:
            log_level = args.get(key)
        if key in ['--log_name', '-ln']:
            log_name = args.get(key)
        if key in ['--log_dir', '-ld']:
            log_dir = args.get(key)

    if not log_level:
        log_level = 'INFO'
    if not log_name:
        log_name = None
    if not log_dir:
        log_dir = os.path.join(get_base_dir(), 'logs')

    log_params = {'log_level': log_level, 'log_name': log_name, 'log_dir': log_dir}

    return log_params


def get_base_dir():
    try:
        base_dir = os.getcwd()
    except:
        base_dir = ''

    return base_dir


def parse_json(json_fname: str, encoding: str = 'utf-8', return_: object = None):
    """
    Parse json file
    :param json_fname: filename which should be parsed
    :param encoding: Encoding
    :return: Dict with json data
    """
    try:
        json_file = open(json_fname, encoding=encoding)
        json_str = json_file.read()
        json_data = json.loads(json_str, object_hook=date_hook)
    except:
        json_data = return_

    return json_data


def date_hook(json_dict: object):
    """
    Hook which used for translate date string in json file to datetime type
    :param json_dict: dict from json file
    :return: dict from json after translating
    """
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict


def create_json(json_fname: str, json_data: object, encoding: str = 'utf-8'):
    """
    Create json file from dict
    :param json_fname: Filename
    :param json_data: Dict which contain data to writing
    :param encoding: Encoding
    :return:
    """
    file_dir, file_name = os.path.split(json_fname)
    if file_dir and file_dir != '' and not os.path.exists(file_dir):
        os.makedirs(file_dir)
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    with open(json_fname, 'w', encoding=encoding) as outfile:
        response = json.dump(json_data, outfile, ensure_ascii=False, default=dthandler, indent=4)


def get_list_files(path: str, filter=None, filter_not_contain: str = None, add_path: bool = False, path2: str = ''):
    """
    Get filelist with path in folder
    :param path: Folder containing files
    :param filter: filter (regexp-like), could be list of str or just str. None by default
    :param add_path: bool, will needed add path to file or not
    :param path2: path which need to add
    :return: return list of files with/without path to it
    """
    path = os.path.normpath(path)
    list_files = []
    if add_path:
        if path2 == '':
            path2 = path
        else:
            path2 = os.path.normpath(path2)
    else:
        path2 = ''

    if filter_not_contain:
        filter = r'^((?!{filter_not_contain}).)*$'.format(filter_not_contain=filter_not_contain)
    if filter:
        if type(filter) == list:
            for f in filter:
                list_files.extend([os.path.join(path2, x) for x in os.listdir(path) if re.search(f, x)])
        if type(filter) == str:
            list_files = [os.path.join(path2, x) for x in os.listdir(path) if re.search(filter, x)]
    else:
        list_files = [os.path.join(path2, x) for x in os.listdir(path)]

    return list_files


def get_progress(pb_i: int, pb_m: int, pb_p: int=10):
    pb_s = pb_m / (100 / pb_p)
    if pb_i == 0:
        log_info('{:4.0f}% ({} / {})'.format(0.0, pb_i, pb_m))
        # return pb_i
    if math.floor((pb_i + 1) % pb_s) == 0:
        log_info('{:4.0f}% ({} / {})'.format((pb_i + 1) / pb_s * pb_p, (pb_i + 1), pb_m))
        return (pb_i + 1) / pb_s * pb_p
    if pb_i == (pb_m - 1):
        log_info('{:4.0f}% ({} / {})'.format(100.0, pb_i + 1, pb_m))
        return (pb_i + 1) / pb_s * pb_p

    return None


def get_double(d: list, key: str):
    D = defaultdict(list)
    d = [x.get(key) for x in d]
    for i, item in enumerate(d):
        D[item].append(i)
    D = {k: v for k, v in D.items() if len(v) > 1}

    return D


def check_folder_exist(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def simple_translit(text: str):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    result = text.translate(tr)
    return result


def encode_password(text: str):
    for offcet in range(1, 10):
        text = caesar_code(text, shift=offcet)
    return text


def decode_password(text: str):
    for offcet in range(9, 0, -1):
        text = caesar_code(text, shift=-offcet)
    return text


if __name__ == '__main__':
    pass
