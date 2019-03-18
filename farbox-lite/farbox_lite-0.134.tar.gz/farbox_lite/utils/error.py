#coding: utf8
from __future__ import absolute_import
import sys
import datetime
import traceback
from farbox_lite import version
from .utils import smart_str



def capture_python_errors_to_local_error_log():
    sys.excepthook = when_error_happened


def when_error_happened(e_type, value, tb):
    # config -> settings -> when_error_happened -> configs; will raise error
    try:
        # 错误信息保存到本地
        log_header = '%s @version capture_error %s' % (str(datetime.datetime.now()), version)
        error_filepath = '/tmp/farbox_lite_error_%s.log' % version
        try:
            with open(error_filepath, 'a') as f:
                content_to_write = '\n%s\n' % log_header
                content_to_write = smart_str(content_to_write)
                f.write(content_to_write)
                traceback.print_exception(e_type, value, tb, file=f)
        except:
            pass
        # print into console
        traceback.print_exception(e_type, value, tb)
    except:
        pass


def capture_error(): # 本身不要再引发错误
    try:
        error_info = sys.exc_info()
        if error_info:
            e_type, value, tb = error_info[:3]
            when_error_happened(e_type, value, tb)
    except:
        pass