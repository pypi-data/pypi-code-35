from pyquilted.quilted.section import Section


class HeadingComplex(Section):
    """The heading section located at the top of a quilted resume

       A complex heading format that is aligned at the sides. It
       supports at most 5 items.
    """
    def __init__(self, name=None, adjacent=None, primary=None,
                 top_side=None, bottom_side=None):
        self.name = name
        self.adjacent = adjacent
        self.primary = primary
        self.top_side = top_side
        self.bottom_side = bottom_side
