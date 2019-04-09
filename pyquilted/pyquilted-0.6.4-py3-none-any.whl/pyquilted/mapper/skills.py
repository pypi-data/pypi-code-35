from pyquilted.quilted.skills import *


class SkillsMapper:
    """Skills data mapper object"""
    def __init__(self, skills_odict):
        self.odict = list(skills_odict)

    def deserialize(self):
        skills = Skills(self.odict)
        return skills
