from pyquilted.quilted.section import Section


class Education(Section):
    """The education section in a quilted resume

       The education object is a compact section that is a string
       describing your education. As a section it mixes in the
       sectionable functionality.
    """
    def __init__(self, education, icon=None):
        self.label = 'Education'
        self.value = education
        self.icon = icon or "fa-graduation-cap"
