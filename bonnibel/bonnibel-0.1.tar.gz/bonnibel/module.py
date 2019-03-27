
class Module:
    def __init__(self, name, output, root, **kwargs):
        from os.path import commonpath, dirname, isdir, join

        self.name = name
        self.output = output
        self.kind = kwargs.get("kind", "exe")
        self.target = kwargs.get("target", None)
        self.deps = kwargs.get("deps", tuple())
        self.includes = kwargs.get("includes", tuple())
        self.defines = kwargs.get("defines", tuple())
        self.depmods = []

        sources = [join(root, f) for f in kwargs.get("source", tuple())]
        modroot = commonpath(sources)
        while not isdir(modroot):
            modroot = dirname(modroot)

        from .source import Source
        self.sources = [Source(f, root, modroot) for f in sources]

    def __str__(self):
        return "Module {} {}\n\t".format(self.kind, self.name)

    def find_depmods(self, modules):
        self.depmods = set()
        open_list = set(self.deps)
        closed_list = set()

        while open_list:
            dep = modules[open_list.pop()]
            open_list |= (set(dep.deps) - closed_list)
            self.depmods.add(dep)

        self.libdeps = [d for d in self.depmods if d.kind == "lib"]
        self.exedeps = [d for d in self.depmods if d.kind != "lib"]

