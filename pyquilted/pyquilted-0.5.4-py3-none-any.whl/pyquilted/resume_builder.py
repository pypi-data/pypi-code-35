from pyquilted.quilted.resume import Resume
from pyquilted.quilted.style import Style
from pyquilted.mapper.section import SectionMapper


class ResumeBuilder:
    """Builder class that has the steps to create a resume from yaml"""
    def __init__(self, resume_odict, style=None, options=None):
        self.resume_odict = resume_odict
        self.resume = Resume(style=style)

    def section_map(self):
        for key, val in self.resume_odict.items():
            mapper = SectionMapper(key, val)
            self.resume.add_section(mapper.create_section())
        return self.resume
