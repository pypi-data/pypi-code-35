#coding: utf8
from __future__ import absolute_import
import os
from farbox_lite.compiler.utils import get_file_list
from .jade2jinja import compile_jade_file
from .css import compile_css_file


def is_file_to_compile(filepath):
    if os.path.isdir(filepath):
        return True
    elif os.path.isfile(filepath):
        ext = os.path.splitext(filepath)[-1].lower()
        if ext in ['.jade', '.less', '.scss']:
            return True
    # at last
    return False


def compile_site_templates(templates_root):
    filepaths = get_file_list(templates_root, filter_func=is_file_to_compile)
    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if ext in ['.less', '.scss']:
            compile_css_file(filepath)
        elif ext == '.jade':
            compile_jade_file(filepath)
