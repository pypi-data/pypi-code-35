from pyquilted.quilted.skills import Skills
from pyquilted.quilted.skills_table import SkillsTable


class SkillsBuilder:
    """Skills data mapper object"""
    def __init__(self, skills_odict, table=False, sorting=True):
        self.odict = list(skills_odict)
        self.table = table
        self.sorting = sorting

    def deserialize(self):
        if self.table:
            skills = SkillsTable(self.odict, sort=self.sorting)
        else:
            skills = Skills(self.odict, sort=self.sorting)
        return skills
