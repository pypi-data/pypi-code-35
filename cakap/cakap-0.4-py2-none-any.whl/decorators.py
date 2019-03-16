__author__ = ('Imam Omar Mochtar', ('iomarmochtar@gmail.com',))

"""
Collection of decorators
"""

import inspect
import traceback
from pprint import pprint
from .utils import Utils

def chelp(desc=None, args=[], is_async=False):
    """
    set help and args for cmd
    """
    def getfunc(f):
        def getresult(*args, **kwargs):
            return f(*args, **kwargs)

        getresult.desc = desc 
        getresult.args = args 
        getresult.is_async = is_async

        return getresult 
    return getfunc 

def auth(f):
    def auth_filter(*args, **kwargs):
        obj, bot, update = args[:3]
        f_name = f.__name__
        if not obj.check_auth(bot, update, f_name):
            return None
        return f(*args, **kwargs)
    return auth_filter 

# catch any error
def catch_error(f):
    def ce_filter(*args, **kwargs):
        obj, bot, update = args[:3]
        try:
            # if it's has arguments then do argument filtering
            if hasattr(f, 'args') and f.args:
                clean_args = obj.filter_args(f.args, kwargs.get('args', []))
                if type(clean_args) == str:
                    Utils.send(bot, update, clean_args, reply=True)
                    return
                kwargs['args'] = clean_args

            result = f(*args, **kwargs)
            # if it's returned string means to reply the message
            if type(result) != str:
                return result

            Utils.send(bot, update, result, reply=True)
            
        except Exception as e:
            err_msg = traceback.format_exc()
            msg = err_msg if obj.debug else 'Please see program\'s log for more detail'
            Utils.send(bot, update, 'ERR: %s'%msg, reply=True)
            obj.error_handler(err_msg)
    
    # make sure it's not called multiple times
    for attr in ['desc', 'args', 'is_async']:
        if not hasattr(ce_filter, attr) and hasattr(f, attr):
            setattr(ce_filter, attr, getattr(f, attr)) 

    return ce_filter 

class AutoSet(type):

    def __init__(cls, name, bases, ns):

        prefix = getattr(cls, 'cmd_prefix')

        for name, val in ns.items():
            # if contain cmd_ as it's suffix and function then assign the decorators (with condition)
            if name.startswith(prefix) and inspect.isfunction(val):

                # mandatory decorator to cache error
                setattr(cls, name, catch_error(val))
