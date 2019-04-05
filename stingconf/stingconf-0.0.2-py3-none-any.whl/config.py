class ConfigMeta():
    pass


class Config():
    def __init__(self):
        self._keys = []
        self.meta = ConfigMeta()

    def add(self, name, value, meta):
        self._keys.append(name)
        setattr(self, name, value)
        setattr(self.meta, name, meta)

    def keys(self):
        for k in self._keys:
            yield k

    def values(self):
        for k in self._keys:
            yield getattr(self, k)

    def items(self):
        for k in self._keys:
            yield k, getattr(self, k)
