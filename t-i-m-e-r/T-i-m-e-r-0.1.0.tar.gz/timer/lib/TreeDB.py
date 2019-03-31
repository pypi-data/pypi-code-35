class _Node:
    def __init__(self, data=None, children=None):
        self.data = data
        self.children = children if children is not None else {}

    def __repr__(self):
        return '{data: %s, children: %s}' % (self.data, self.children)


class TreeDB:
    def __init__(self):
        self._d = _Node()

    def __getitem__(self, key):
        d = self._d
        try:
            for k in [_ for _ in key.split('/') if _ != '']:
                d = d.children[k]
        except KeyError:
            raise KeyError(key)

        return d.data

    def get(self, key, value=None):
        try:
            return self[key]
        except KeyError:
            return value

    def __setitem__(self, key, value):
        d = self._d
        for k in [_ for _ in key.split('/') if _ != '']:
            if k not in d.children:
                d.children[k] = _Node()
            d = d.children[k]

        d.data = value

    def __repr__(self):
        return str(self._d)
