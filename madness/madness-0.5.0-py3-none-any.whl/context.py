
from werkzeug.local import Local, LocalManager, LocalProxy, LocalStack

local = Local()
local_manager = LocalManager([local])
request = local('request')
context = local('context')

class Context(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __contains__(self, key):
        return hasattr(self, key)
