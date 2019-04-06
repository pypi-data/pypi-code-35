class Feature:
    def __init__(self, name, dependencies={}, code=""):
        self._name = name
        self._code = code
        self._dependencies = dependencies

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    def dependencies(self, key):
        return self._dependencies.get(key, [])

    def __eq__(self, other):
        return (isinstance(other, Feature) and
                other.name == self._name)

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return f"Feature({self._name})"
