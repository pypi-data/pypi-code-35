class ConfigMeta():
    pass


class Config():
    def __init__(self):
        self.meta = ConfigMeta()

    def add(self, name, value, meta):
        setattr(self, name, value)
        setattr(self.meta, name, meta)
