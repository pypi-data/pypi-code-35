#coding: utf8
from __future__ import absolute_import
from jinja2.runtime import Context, Undefined, Macro
from jinja2.compiler import CodeGenerator
from werkzeug.exceptions import HTTPException

from farbox_lite.utils import smart_unicode
from farbox_lite.template_system.functions.namespace import default_variables


old_context_call = Context.call


# context resolve是全局性的hack
def context_resolve(self, key):
    if key in self.vars:
        return self.vars[key]
    if key in self.parent:
        return self.parent[key]

    key_lower = key.lower()
    if key in default_variables: # 全局的变量匹配，实际上都是函数
        return default_variables[key]
    elif key_lower in default_variables:
        return default_variables[key_lower]

    # at last
    return self.environment.undefined(name=key)



def context_call(self, context_obj, *args, **kwargs):
    # 一般只是本地的 jade 才会调用到，外部的实际走evn_call
    if not hasattr(context_obj, '__call__'): # 不可 call, 可能仅仅是 property
        return context_obj
    try:
        value = old_context_call(self, context_obj, *args, **kwargs)
        if value is None:
            value = Undefined()
        return value
    except HTTPException, e:
        raise  e
    except TypeError, e:
        if hasattr(e, 'message') and 'not callable' in e.message:
            # 被调用的函数不可被call，返回原始值
            return context_obj
        else:
            # sentry_client.captureException()
            message = getattr(e, 'message', None) or ''
            if message:
                return message
            error_info = 'context_call error:* %s, ** %s; %s' % (smart_unicode(args), smart_unicode(kwargs), message)
            return error_info
    except Exception, e:
        if isinstance(context_obj, Macro):
            pass
        else:
            # todo should captureException?
            pass

        message = getattr(e, 'message', None) or ''
        object_name = getattr(context_obj, '__name__', None) or ''
        if message:
            error_info = message
        else:
            error_info = 'context_call error: %s, * %s, ** %s; %s' % (object_name, smart_unicode(args), smart_unicode(kwargs), message)

        return '<error>%s</error>' % error_info




Context.resolve = context_resolve
Context.call = context_call


old_visit_name_func = CodeGenerator.visit_Name

def visit_name(self, node, frame):
    if node.name in default_variables and node.ctx=='load':
        # 默认变量最终转化为 call 的模式，因为本身就是函数，这样不会改变模板内代码整体的执行次序
        self.write("environment.call(context, l_%s)" % node.name)
    else:
        old_visit_name_func(self, node, frame)


CodeGenerator.visit_Name = visit_name

