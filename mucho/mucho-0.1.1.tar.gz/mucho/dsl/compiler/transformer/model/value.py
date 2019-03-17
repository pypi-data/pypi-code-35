from typing import Union


class Value:
    """Basic type value of the DSL, e.g. a float number."""

    def __init__(self, value: Union[float, bool]):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)
