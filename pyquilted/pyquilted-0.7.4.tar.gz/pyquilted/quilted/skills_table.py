from pyquilted.quilted.table import Table
from pyquilted.quilted.section import Section
from pyquilted.quilted.skills import Sorted


class SkillsTable(Section, Sorted):
    """The skills section in a quilted resume

       The skills object is a compact section that is a comma separated
       list of strings describing your skills. As a section it mixes in
       the sectionable functionality.
    """
    def __init__(self, skills, icon=None, cols=4, default="", sort=True):
        self.sort = sort
        self.label = 'Skills'
        self.icon = icon or "fa-wrench"
        self.rows = Table(cols=cols, default=default).build(
                self.sort_list(skills))
        self.compact = False
