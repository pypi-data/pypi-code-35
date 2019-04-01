from pyquilted.quilted.section import Section


class Skills(Section):
    """The skills section in a quilted resume

       The skills object is a compact section that is a comma separated
       list of strings describing your skills. As a section it mixes in
       the sectionable functionality.
    """
    def __init__(self, skills, icon=None):
        self.label = 'Skills'
        self.value = ", ".join(skills)
        self.icon = icon or "fa-wrench"
