from pyquilted.quilted.resume import Resume
from pyquilted.builder.section_factory import SectionBuilderFactory


class ResumeBuilder:
    """Builder class that has the steps to create a resume from yaml"""
    def __init__(self, resume_odict, style_options=None, section_options=None):
        self.resume_odict = resume_odict
        self.resume = Resume(style=style_options)
        self.section_options = section_options

    def section_map(self):
        for key, val in self.resume_odict.items():
            builder = SectionBuilderFactory(key, val, options=self.section_options)
            self.resume.add_section(builder.create_section())
        return self.resume
