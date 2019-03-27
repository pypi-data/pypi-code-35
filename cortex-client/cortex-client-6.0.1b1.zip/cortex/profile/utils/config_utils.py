__all__ = [
    'AttrsAsDict',
]

class _AttrsAsDictMeta(type):
    """
    Meta class to help transform any python class that extends this type into a dict where the keys are the attributes
    of the class and the values are the respected attribute values.

    This class is useful in place of enums, where we want an IDE to auto fill in attributes, but we want to treat the
    class like a dict as well.
    """
    def __iter__(self):
        return zip(self.keys(), self.values())

    def __getitem__(self, arg):
        return dict(list(self)).get(arg)

    def keys(cls):
        return list(filter(lambda x: x[0] != "_", cls.__dict__.keys()))

    def values(cls):
        return [ getattr(cls, k) for k in cls.keys()]

    def items(cls):
        return dict(list(cls)).items()


class AttrsAsDict(metaclass=_AttrsAsDictMeta):
    """
    Any class that extends this will have its attributes be transformable into a dict.
    """
    pass