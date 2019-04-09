from pyquilted.quilted.section import Section


class Sorted:
    def sort_list(self, items):
        if self.sort:
            return sorted(items)
        return items


class Skills(Section, Sorted):
    """The skills section in a quilted resume

       The skills object is a compact section that is a comma separated
       list of strings describing your skills. As a section it mixes in
       the sectionable functionality.
    """
    def __init__(self, skills, icon=None, sort=True):
        self.sort = sort
        self.label = 'Skills'
        self.value = ", ".join(self.sort_list(skills))
        self.icon = icon or "fa-wrench"
        self.compact = True
