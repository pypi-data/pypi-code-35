class ComparisonResult:
    """Result of a comparison between 2 or more entities."""

    def __init__(self, **kwargs):
        """
        :param kwargs: names of the properties of the comparison result along
        with their values
        """
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)

    def __repr__(self):
        return str(self)
