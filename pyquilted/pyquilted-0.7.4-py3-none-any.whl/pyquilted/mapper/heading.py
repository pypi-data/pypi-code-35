from pyquilted.mapper.details import HeadingDetailsMapper
from pyquilted.quilted.heading_complex import HeadingComplex
from pyquilted.quilted.heading_simple import HeadingSimple


class HeadingMapper:
    """Heading data mapper object"""
    def __init__(self, odict):
        self.heading = HeadingDetailsMapper(odict).deserialize()
        self.section = None

    def deserialize(self):
        if self.heading.objective or len(self.heading.details) > 2:
            self._build_heading_complex()
        else:
            self._build_heading_simple()
        return self.section

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
        else:
            self.section = HeadingComplex(name=self.heading.name,
                                          primary=self.heading.details[0],
                                          top_side=self.heading.details[1],
                                          bottom_side=self.heading.details[2]
                                          )

    def _build_heading_simple(self):
        if len(self.heading.details) == 2:
            self.section = HeadingSimple(name=self.heading.name,
                                         adjacent=self.heading.details[0],
                                         primary=self.heading.details[1])
        elif len(self.heading.details) == 1:
            self.section = HeadingSimple(name=self.heading.name,
                                         primary=self.heading.details[0])
        else:
            self.section = HeadingSimple(name=self.heading.name)
