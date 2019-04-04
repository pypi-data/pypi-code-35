
from dataclasses import dataclass

from werkzeug.local import Local, LocalManager, LocalProxy, LocalStack

local = Local()
local_manager = LocalManager([local])
request = local('request')
g = local('g')

class G(object):
    """user managed request context
    """

    def __contains__(self, key):
        return hasattr(self, key)
