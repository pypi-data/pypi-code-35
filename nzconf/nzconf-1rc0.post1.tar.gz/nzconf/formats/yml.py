__all__ = ['YamlFile']
try:
    from yaml.cyaml import CSafeLoader as Loader, CSafeDumper as Dumper
except ImportError: # pragma: no cover
    try:
        from yaml import SafeLoader as Loader, SafeDumper as Dumper
    except ImportError:
        __all__ = []

if __all__:
    import yaml
    from collections import OrderedDict
    from . import _dict_update,_flatten,File,register_extension

    # def dict_representer(dumper,data):
        # return dumper.represent_dict(data.items())
    # Dumper.add_representer(OrderedDict,dict_representer)

    @register_extension('.yml')
    @register_extension('.yaml')
    class YamlFile(File):
        def _dump(self,obj,stream=None):
            with stream or self.open('w') as cfgfile:
                yaml.dump(_flatten(obj),Dumper=Dumper,
                        stream=cfgfile,default_flow_style=False,
                        indent=2)
        def _load(self,obj=None,stream=None):
            with stream or self.open('r') as cfgfile:
                out = yaml.load(cfgfile,Loader=Loader)
            return _dict_update(obj or {}, out)
