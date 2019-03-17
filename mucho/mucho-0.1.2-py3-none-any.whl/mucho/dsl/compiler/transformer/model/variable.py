class Variable:
    """Variable of the DSL, identified by a field and a property name,
    e.g. "movie.year".
    """

    def __init__(self, field: str, property: str, type=None):
        """
        :param field: part before the dot in the variable name
        :param property: part after the dot in the variable name
        :param type: type of the variable
        """
        self.field = field
        self.property = property
        self.type = type

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)
