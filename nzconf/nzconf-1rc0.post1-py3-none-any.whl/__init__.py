try:
    from .__version__ import VERSION
except:               # pragma: no cover
    VERSION='unknown'

from .file import File
from collections import OrderedDict

_EXTENSION2CLASS = OrderedDict()
def _add_extension(k,v):
    global _EXTENSION2CLASS
    d = dict(_EXTENSION2CLASS)
    d[k] = v
    _EXTENSION2CLASS = OrderedDict(sorted(d.items(),key=lambda x: len(x[0]),reverse=True))

def register_extension(ext,cls=None):
    def _register_extension(c):
        if not issubclass(c,File):
            raise TypeError("Class '%s' must extend '%s'." % (c.__name__,File.__name__))
        # _EXTENSION2CLASS[ext] = c
        _add_extension(ext,c)
        return c
    if cls is None:
        return _register_extension
    return _register_extension(cls)

from . import formats

def supports(ext=None):
    if ext is None:
        return list(_EXTENSION2CLASS.keys())
    return ext in _EXTENSION2CLASS

def AutoFile(filename,*args,**kwargs):
    fn = str(filename)
    for ext,cls in _EXTENSION2CLASS.items():
        if fn.endswith(ext):
            break
    else:
        raise KeyError("Unsupported extension for '%s'." % fn)
    return cls(filename,*args,**kwargs)

__all__ = ['File','register_extension','supports','AutoFile','formats']
