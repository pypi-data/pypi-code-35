class OptCategory:
    """
    A container to hold options. For simplicity, all options have to be stored in an
    OptCategory. If the category description (in the 'category' field) is not provided,
    then no category prints in the usage instructions. Otherwise the options are
    grouped in the usage instructions using the supplied category.
    """
    def __init__(self, category):
        self._category = category
        self._options = []

    @property
    def category(self):
        return self._category

    @property
    def options(self):
        return self._options
