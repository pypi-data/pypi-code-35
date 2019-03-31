__all__=['JsonFile']
try:
    import json
except ImportError: # pragma: no cover
    __all__=[]

if __all__:
    from . import _dict_update,_flatten,File,register_extension
    from io import TextIOWrapper,BytesIO

    @register_extension('.js')
    @register_extension('.json')
    class JsonFile(File):
        def _dump(self,obj,
                stream=None,separators=(',',': '),
                indent=2,newline=True):
            with stream or self.open('w') as cfgfile:
                json.dump(_flatten(obj),cfgfile,
                        separators=separators,indent=indent)
                if newline:
                    cfgfile.write('\n')
        def _load(self,obj=None,stream=None):
            io = TextIOWrapper(BytesIO())
            with stream or self.open('r') as cfgfile:
                size = io.write(cfgfile.read())
            out = {}
            if size:
                io.seek(0)
                out = json.load(io)
            return _dict_update(obj or {}, out)
