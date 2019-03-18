# coding: utf8
from __future__ import absolute_import
from jinja2.environment import Environment
from jinja2.sandbox import SandboxedEnvironment
from jinja2.exceptions import UndefinedError, TemplateNotFound, SecurityError
from jinja2.runtime import Undefined
from werkzeug.exceptions import HTTPException
from flask import abort
import datetime, inspect
import types

from farbox_lite.template_system.func import get_functions_in_a_file_obj, AttrFunc
from farbox_lite.utils.functional import curry

from farbox_lite.template_system.functions import attr_patches
from farbox_lite.template_system.functions.attr_patches.models.date import Date
from farbox_lite.template_system.functions.attr_patches.models.text import Text

from farbox_lite.template_system.utils import return_error_message
from farbox_lite.utils.error import capture_error



all_functions = get_functions_in_a_file_obj(attr_patches.all_functions)
array_functions = get_functions_in_a_file_obj(attr_patches.array_functions)
dict_functions = get_functions_in_a_file_obj(attr_patches.dict_functions)
str_functions = get_functions_in_a_file_obj(attr_patches.str_functions)
date_functions = get_functions_in_a_file_obj(attr_patches.date_functions)

# 特定类型的数据，如果请求其 attr，可以找到对应的functions 进行处理
# 用isinstance(obj, (1,2) or 1) 来判断的，所以是以下的 match table 格式
func_match_rules = [
    [(list, tuple), array_functions],
    [dict, dict_functions],
    ((str, unicode), str_functions),
    [datetime.datetime, date_functions],
]



def render_attr_func_without_call(func): # h.xxx 这样的函数可以直接当做属性处理
    if not hasattr(func, '__call__') or not func:
        return func
    if getattr(func, 'is_attr_func', False):
        return func
    new_func = AttrFunc(func)
    return new_func



def get_attr_func(obj, attr, functions):
    # 在一个指定的functions 的 dict 中，试图取得obj.attr 时，返回对应的 function（如果有的话）
    first_arg = None # 被调用的时候隐含的参数，比如posts.sort_by_date, 其中实际调用的是posts.sort 这个属性
    original_func = None
    if attr in functions:
        original_func = functions[attr]
    elif '_by_' in attr: # posts.sort_by_date('-')
        name, first_arg = attr.split('_by_', 1)
        if name in functions:
            original_func = functions[name]
    if original_func:
        wrapped_func = curry(original_func, obj)
        # 不能被 wrap 的函数
        if hasattr(original_func, 'arg_spec'):
            # 比如返回一个 dict(如 humech)，就不能是一个 function 了，或者指定了就是一个属性
            args_length = len(original_func.arg_spec.args)
            if args_length == 1 and not original_func.arg_spec.varargs and not original_func.arg_spec.keywords:
                # 原函数仅仅接收一个参数
                return wrapped_func()
            elif not args_length:
                # 不接受任何参数的， curry 都是不行的, 其实就是相当于一个属性（的函数运行）
                return original_func()
        return wrapped_func


old_getattr_func = Environment.getattr
sandbox_getattr_func = SandboxedEnvironment.getattr
allowed_fields = ['_id', ]
def env_getattr(self, obj, attr, sandbox=False):

    # 是否是 API 本提供的属性
    is_namespace_field = False
    if attr.startswith('_') and '__' not in attr and not isinstance(obj, dict) and attr not in allowed_fields:
        try:
            obj_name = obj.__class__.__module__
            if 'farbox_lite.template_system.functions.namespace.' in obj_name:
                is_namespace_field = True
        except:
            pass

    # 字符串其实比较常用，避免过度解析
    # tryText是 attr 以_结尾 或者 attr 本身的名称为 content

    if attr in allowed_fields:
        getattr_func = old_getattr_func
    elif isinstance(obj, dict) and attr in obj:
        getattr_func = old_getattr_func
    elif is_namespace_field:
        getattr_func = old_getattr_func
    elif sandbox:
        getattr_func = sandbox_getattr_func
    else:
        getattr_func = old_getattr_func

    if attr.startswith('__'):
        return ''


    if attr.endswith('_'):
        try_Text = True
        attr = attr[:-1]
    else:
        if attr in ['content']:
            try_Text = True
        else:
            try_Text = False

    #if isinstance(obj, (str, unicode)): # obj 本身就是字符串的情况
    #    _obj = Text(obj)
    #    if hasattr(_obj, attr): # 比如 '123'.int
    #        return getattr(_obj, attr)
    #    else: # 比如 'abc'.title
    #        old_getattr_func_value = getattr_func(self, obj, attr)
    #        if not isinstance(old_getattr_func_value, Undefined):
    #            return old_getattr_func_value

    try_patch = False
    try:
        value = getattr_func(self, obj, attr)
        if isinstance(value, Undefined):
            try_patch = True
        elif hasattr(value, '__call__'):
            try_patch = True
    except UndefinedError:
        value = '' # by default
        try_patch = True

    # 这里应该触发错误, 如果不是UndefinedError 的话

    if isinstance(value, Undefined):
        try_patch = True

    # 使用数据类型的 class 直接进行处理
    if isinstance(value, datetime.datetime):
        return Date(value)
    elif isinstance(value, (str, unicode)) and try_Text:
        return Text(value, attr=attr, parent=obj)

    # 必须被 patch 的一些属性
    if not try_patch and isinstance(obj, (Text, Date)) and not hasattr(obj, attr):
        try_patch = True

    if try_patch:
        # 出现 UndefinedError 或者本身就是 Undefined， 那么放心大胆的 patch
        # 另外 函数的patch 优先级高于原生的，比如insert 对于一个 array
        all_matched_func = get_attr_func(obj, attr, all_functions)
        if all_matched_func:
            return all_matched_func
        for func_types, functions in func_match_rules:
            if isinstance(obj, func_types):
                matched_func = get_attr_func(obj, attr, functions)
                if matched_func is not None:
                    return matched_func

    if hasattr(value, '__call__') and value and hasattr(obj, '__class__') and \
            isinstance(value, (types.FunctionType, types.MethodType)):
        # 只有默认变量的一些子属性才有这样的功能
        obj_class = obj.__class__
        if hasattr(obj_class, '__module__'):
            obj_module = obj_class.__module__
            if isinstance(obj_module, (str, unicode)) and obj_module.startswith('farbox_lite.template_system.functions.namespace.'):
                value = render_attr_func_without_call(value)

    if value is None:
        value = ''

    return value

# patch
def env_call(self, context, context_obj, *args, **kwargs):
    # 实际上是要求运行obj(这个函数）, 默认变量都是进行 call的，以保证 jinja2 解析后的代码执行次序
    if not context_obj: # maybe Undefined
        return context_obj
    if not hasattr(context_obj, '__call__') and not args and not kwargs:
        return context_obj
    if getattr(context_obj, 'was_called', False):
        # 比如 site = site or something, 会导致 site 被多次 call...
        return context_obj

    # 不能被 call 的，本身就是函数，需要在模板里被调用
    # 因为所有变量都会被 call，在赋值的时候；而函数类型的，是后续要调用的，直接被 call 的话，获得类型就不对了，不再是函数，就没有办法在 api 里调用了。
    # env_call 跟 get_attr 又不一样，它更多是一级的变量调用，get_attr 是获取属性
    # context_obj_name = getattr(context_obj, '__name__', None)
    # (args, varargs, keywords, defaults). args is a list of the argument names (it may contain nested lists). varargs and keywords are the names of the * and ** arguments or None
    if not args and not kwargs and hasattr(context_obj, 'arg_spec') and context_obj.arg_spec:
        if context_obj.arg_spec.args or context_obj.arg_spec.varargs or context_obj.arg_spec.keywords:
            return context_obj # like i18n

    try:
        result = context.call(context_obj, *args, **kwargs)
        if not hasattr(result, '__call__'):
            try: setattr(result, 'was_called', True) # 一些变量
            except: pass
        return result
    except HTTPException, e:
        raise e
    except Exception, e:
        if isinstance(context_obj, (unicode, str, list, tuple, int, float)): # 基础数据类型，call的时候，返回其本身
            return context_obj
        error_info = "%s not a valid function, can't be called, error_info: %s" % (getattr(context_obj, 'func_name', ''), e.message)
        return return_error_message(error_info)


old_env_handle_exception = Environment.handle_exception
def env_handle_exception(self, exc_info=None, rendered=False, source_hint=None):
    # source_hint 是编译后的 jinja2 模板
    source_hint = source_hint or ''
    if not rendered:
        error = exc_info[1]
        filename = error.filename or ''
        if filename.endswith('.jade'):
            filename = '<a href="/service/template_code/%s">compiled %s</a>, ' \
                       'the line number may be different to your own code' % (filename, filename)
        error_information = "template file: %s \n line number:%s \n error message: %s" % (
            filename,
            error.lineno,
            error.message
        )
        error_info = dict(lineno=error.lineno, source=source_hint, message=error_information, debug=True)
        abort(500, error_info)
    elif exc_info[0] in [TemplateNotFound]:
        error_information = '%s TemplateNotFound' % exc_info[1].message
        abort(500, error_information)
    elif exc_info[0] in [UndefinedError, ValueError, TypeError]:
        capture_error()
        error_information = exc_info[1].message
        abort(500, error_information)
    else:
        # 这里不要尝试直接 500， 有可能是 redirect 或者其它错误
        return old_env_handle_exception(self, exc_info, rendered, source_hint)

Environment.getattr = env_getattr
Environment.call = env_call
Environment.handle_exception = env_handle_exception
