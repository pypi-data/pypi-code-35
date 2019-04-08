# Used for micro service developed by nameko
# Have to install nameko
"""
    Example::

        from wisdoms.auth import permit

        host = {'AMQP_URI': "amqp://guest:guest@localhost"}

        auth = permit(host)

        class A:
            @auth
            def func():
                pass
"""

from nameko.standalone.rpc import ClusterRpcProxy
from nameko.rpc import rpc
from wisdoms.utils import xpt_func
from functools import wraps


def permit(host):
    """ 调用微服务功能之前，进入基础微服务进行权限验证

    :param: host: micro service host
    """

    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            srv_name = args[0].name
            uid = args[1]['uid']
            f_name = f.__name__
            with ClusterRpcProxy(host) as rpc:
                res = rpc.db_service.isrole_app(srv_name, uid, f_name)
            if res['code'] == 1:
                return f(*args, **kwargs)
            return res

        return inner

    return wrapper


def ms_base(ms_host):
    """
    返回父类，闭包，传参数ms host
    :param ms_host:
    :return:
    """

    class MsBase:
        name = 'ms-base'

        @rpc
        @xpt_func
        def into_base(self):
            clazz = type(self)
            name = clazz.name
            functions = list(clazz.__dict__.keys())
            with ClusterRpcProxy(ms_host) as r:
                r.db_service.into_base(name, functions)

    return MsBase


def assemble(rpc, service, function1, param1='', *params):
    str1 = rpc + '.' + service + '.' + function1
    str2 = '(' + param1
    for param in params:
        str2 += ',' + param
    str2 += ')'
    return str1 + str2


def crf_closure(ms_host):
    def crf(service, function1, data):
        with ClusterRpcProxy(ms_host) as rpc:
            result = eval(assemble('rpc', service, function1, 'data'))
        return result

    return crf
