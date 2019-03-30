
class Source:
    Actions = {'.c': 'cc', '.cpp': 'cxx', '.s': 'nasm'}

    def __init__(self, path, root, modroot):
        from os.path import relpath, splitext
        self.input = path
        self.name = relpath(path, root)
        self.output = relpath(path, modroot) + ".o"
        self.action = self.Actions.get(splitext(path)[1], None)

    def __str__(self):
        return "{} {}:{}:{}".format(self.action, self.output, self.name, self.input)

