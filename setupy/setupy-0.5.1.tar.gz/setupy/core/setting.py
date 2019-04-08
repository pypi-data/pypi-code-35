class Setting:

    def __init__(self, name, properties={}, dependencies={}):
        self._name = name
        self._properties = properties
        self._dependencies = dependencies

    @property
    def name(self):
        return self._name

    @property
    def properties(self):
        return self._properties

    def dependencies(self, key):
        return self._dependencies.get(key, [])

    def __eq__(self, other):
        return isinstance(other, Setting) and other.name == self._name

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return f"Setting({self._name})"
