from pyquilted.builder.contacts import ContactsBuilder
from pyquilted.builder.education import EducationBuilder
from pyquilted.builder.heading import HeadingBuilder
from pyquilted.builder.projects import ProjectsBuilder
from pyquilted.builder.skills import SkillsBuilder
from pyquilted.builder.work import WorkBuilder


class SectionBuilderFactory:
    """A data mapper object for all sections"""
    def __init__(self, key, section_odict, options=None):
        self.key = key
        self.section_odict = section_odict
        self.options = options or SectionOptions()
        self.mapper = None
        self.section = None

    def create_section(self):
        self._create_mapper()
        self.section = self.mapper.deserialize()
        return self.section

    def _create_mapper(self):
        if self.key in 'contacts':
            self.mapper = ContactsBuilder(self.section_odict)
        elif self.key in 'education':
            self.mapper = EducationBuilder(self.section_odict)
        elif self.key in 'heading':
            self.mapper = HeadingBuilder(self.section_odict,
                                         heading_type=self.options.heading)
        elif self.key in 'projects':
            self.mapper = ProjectsBuilder(self.section_odict)
        elif self.key in 'skills':
            self.mapper = SkillsBuilder(self.section_odict,
                                        table=self.options.skills_table,
                                        sorting=self.options.sorting)
        elif self.key in 'work':
            self.mapper = WorkBuilder(self.section_odict)


class SectionOptions:
    """section builder options for the formatting of the sections"""
    def __init__(self, heading_compact=False, heading_expanded=False,
            skills_table=False, sorting=True, **kwargs):
        self.skills_table = skills_table
        self.sorting = sorting
        self._set_heading(heading_expanded, heading_compact)

    def _set_heading(self, expanded, compact):
        if expanded:
            self.heading = 'complex'
        elif compact:
            self.heading = 'compact'
        else:
            self.heading = 'auto'
