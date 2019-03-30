# -*- coding: utf-8 -*-

try:
    import importlib.resources as res
except ImportError:  # pragma: no-cover
    import importlib_resources as res


def read_text(resource_name):
    '''
    Get resource

    :param resource_name: name of resource to load
    :type resource_name: str
    :returns: decoded resource content
    :type: str
    '''
    return res.read_text(__name__, resource_name)
