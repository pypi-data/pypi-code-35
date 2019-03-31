__all__=['IniFile']
try:
    import configparser
except ImportError: # pragma: no cover
    __all__=[]

if __all__:
    from . import _dict_update,_flatten,File,register_extension
    from io import TextIOWrapper,BytesIO

    def cp2dict(cp):
        return dict(filter(lambda x: len(x[1]),
                    map(lambda x: (x[0],dict(x[1])),
                        cp.items())))
    def any2cp(obj):
        if obj is None:
            return configparser.ConfigParser()
        if isinstance(obj,configparser.ConfigParser): # pragma: no cover
            return obj
        cp = configparser.ConfigParser()
        cp.read_dict(obj)
        return cp

    @register_extension('.ini')
    class IniFile(File):
        def _dump(self,obj,stream=None):
            cfg = any2cp(_flatten(obj))
            with stream or self.open('w') as cfgfile:
                cfg.write(cfgfile)
        def _load(self,obj=None,stream=None):
            cfg = any2cp(obj)
            with stream or self.open('r') as cfgfile:
                cfg.read_file(cfgfile)
            return cp2dict(cfg)
