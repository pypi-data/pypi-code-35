from pyquilted.builder.details import HeadingDetailsBuilder
from pyquilted.quilted.heading_complex import HeadingComplex
from pyquilted.quilted.heading_simple import HeadingSimple


class HeadingBuilder:
    """Heading data mapper object"""
    def __init__(self, odict, heading_type=None):
        self.heading = HeadingDetailsBuilder(odict).deserialize()
        self.section = None
        self.format = heading_type or 'auto'

    def deserialize(self):
        if self.format == 'complex':
            self._build_heading_complex()
        elif self.format == 'compact':
            self._build_heading_simple()
        else:
            self._build_heading_auto()

        return self.section

    def _build_heading_auto(self):
        if self.heading.objective or len(self.heading.details) > 2:
            self._build_heading_complex()
        else:
            self._build_heading_simple()

    def _build_heading_complex(self):
        if self.heading.objective and len(self.heading.details) == 3:
            self.section = HeadingComplex(name=self.heading.name,
                                          primary=self.heading.objective,
                                          adjacent=self.heading.details[0],
                                          top_side=self.heading.details[1],
                                          bottom_side=self.heading.details[2]
                                          )
        elif self.heading.objective and len(self.heading.details) == 2:
            self.section = HeadingComplex(name=self.heading.name,
                                          primary=self.heading.objective,
                                          top_side=self.heading.details[0],
                                          bottom_side=self.heading.details[1]
                                          )
        elif self.heading.objective and len(self.heading.details) == 1:
            self.section = HeadingComplex(name=self.heading.name,
                                          primary=self.heading.objective,
                                          top_side=self.heading.details[0]
                                          )
        elif len(self.heading.details) == 3:
            self.section = HeadingComplex(name=self.heading.name,
                                          primary=self.heading.details[0],
                                          top_side=self.heading.details[1],
                                          bottom_side=self.heading.details[2]
                                          )
        elif len(self.heading.details) == 2:
            self.section = HeadingComplex(name=self.heading.name,
                                          primary=self.heading.details[0],
                                          top_side=self.heading.details[1]
                                          )
        elif len(self.heading.details) == 1:
            self.section = HeadingComplex(name=self.heading.name,
                                          top_side=self.heading.details[0]
                                          )
        elif self.format == 'complex':
            self.section = HeadingComplex(name=self.heading.name)


    def _build_heading_simple(self):
        if len(self.heading.details) >= 2:
            self.section = HeadingSimple(name=self.heading.name,
                                         adjacent=self.heading.details[0],
                                         primary=self.heading.details[1])
        elif len(self.heading.details) == 1:
            self.section = HeadingSimple(name=self.heading.name,
                                         primary=self.heading.details[0])
        else:
            self.section = HeadingSimple(name=self.heading.name)
