# coding: utf8
from __future__ import absolute_import
from werkzeug.exceptions import HTTPException
from jinja2.runtime import Undefined

from farbox_lite.utils import smart_unicode, UnicodeWithAttrs



def return_error_message(message):
    if 'error_ignored' in message:
        error_info = UnicodeWithAttrs('')
    else:
        error_info = UnicodeWithAttrs('<span style="color:red" class="template_api_error">&lt;%s&gt:</span>' % message)
    error_info.is_error = True
    return error_info



def run_function_safely(func):
    def _func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException, e:
            raise e
        except Exception, e:
            message = '`%s` usage error @ %s' % (getattr(func, 'func_name', 'function'), getattr(type(e), '__name__', ''))
            e_message = getattr(e, 'message', '')
            if e_message:
                message = '%s: %s' % (message, smart_unicode(e_message))
            return return_error_message(message)
    return _func






class SafeUndefined(Undefined):
    # 直接融入到用户的API渲染的页面中，我们自己程序中不做callback
    def __init__(self, *args, **kwargs):
        self._empty_list = []
        Undefined.__init__(self, *args, **kwargs)

    def __iter__(self):
        return self._empty_list.__iter__()

    def _fail_with_undefined_error(self, *args, **kwargs):
        return self

    def __getattr__(self, name):
        return self

    __add__ = \
    __radd__ = \
    __getitem__ = \
    __sub__ = \
    __mul__ = \
    __div__ = \
    __lt__ = \
    __le__ = \
    __gt__ = \
    __ge__ = _fail_with_undefined_error

    def __call__(self, *args, **kwargs):
        if self._undefined_name in ['caller', 'join', 'json', 'content']:
            return ''
        return return_error_message('`%s` is not a valid function' % self._undefined_name)


    def __repr__(self):
        return 'SafeUndefined'