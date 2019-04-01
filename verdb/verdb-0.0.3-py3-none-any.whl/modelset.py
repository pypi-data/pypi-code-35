from collections import OrderedDict


class ModelSet:
    def __init__(self, model, selector, version=None):
        self.model = model
        self.selector = selector
        self.references = OrderedDict()
        self.version = version
        self.refresh()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '[' + ', '.join(f'<{type(ref).__name__}: {ref!r}>' for ref in self.references.values()) + ']'

    def __iter__(self):
        return iter(self.references.values())

    def __len__(self):
        return len(self.references)

    def __contains__(self, key):
        if not isinstance(key, tuple):
            key = (key, None)

        return key in self.references

    def __getitem__(self, key):
        if isinstance(key, slice):
            keys = list(self.references.keys())[key]
            references = OrderedDict((key, self.references[key]) for key in keys)
            return type(self)(self.model, lambda: references, self.version)

        elif isinstance(key, int):
            qualified_key = list(self.references.keys())[key]

        elif isinstance(key, str):
            qualified_key = (key, None)

        elif isinstance(key, tuple):
            qualified_key = key
        else:
            raise ValueError(key)

        if qualified_key in self.references:
            return self.references[qualified_key]
        else:
            raise KeyError(key)

    def __delitem__(self, key):
        instance = self.references[key]
        instance.delete()
        self.references = OrderedDict((key, ref) for key, ref in self.references.items() if ref is not instance)

    def refresh(self):
        self.references = OrderedDict(self.selector())
