from .. import File,register_extension
import contextlib

def _flatten(obj):
    if obj is None:
        return obj
    if isinstance(obj,(str,int,float,bool)):
        return obj
    if isinstance(obj,list):
        return list(map(_flatten,obj))
    if hasattr(obj,'items'):
        return dict(map(lambda x: (x[0],_flatten(x[1])), obj.items()))
    if hasattr(obj,'keys'):
        return dict(map(lambda x: (x,_flatten(obj[x])), obj.keys()))
    return str(obj)

def _dict_update(d,s):
    if hasattr(s,'keys'):
        for k in s.keys():
            d[k] = _dict_update(d.get(k,{}),s[k])
        return d
    return s

__all__ = []

with contextlib.suppress(ImportError):
    from .js import JsonFile
    __all__.append('JsonFile')
with contextlib.suppress(ImportError):
    from .yml import YamlFile
    __all__.append('YamlFile')
with contextlib.suppress(ImportError):
    from .ini import IniFile
    __all__.append('IniFile')
