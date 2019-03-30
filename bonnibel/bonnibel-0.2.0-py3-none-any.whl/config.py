
class Config(object):
    def __init__(self, filename):
        from os.path import abspath, dirname
        from yaml import load
        from .module import Module

        root = dirname(filename)
        confdata = load(open(filename, "r"))

        self.name = confdata['name']
        self.templates = confdata['templates']

        self.vars = confdata.get('vars', {})

        self.modules = {}
        for name, data in confdata['modules'].items():
            self.modules[name] = Module(name, root=root, **data)

        for mod in self.modules.values():
            mod.find_depmods(self.modules)

        self.targets = {}
        for mod in self.modules.values():
            if mod.target is None: continue
            if mod.target not in self.targets:
                self.targets[mod.target] = set()
            self.targets[mod.target].add(mod)
            self.targets[mod.target] |= mod.depmods

