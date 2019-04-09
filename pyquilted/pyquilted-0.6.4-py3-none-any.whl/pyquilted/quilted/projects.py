from pyquilted.quilted.section import Section


class Projects(Section):
    """The project section in a quilted resume

       The project object is a complex section. It contains blocks of
       activities. As a section it mixes in the sectionable functionality.
    """
    def __init__(self, blocks=None, icon=None):
        self.label = 'Projects'
        self.icon = icon or "fa-code"
        self.blocks = blocks or []

    def add_activity(self, activity):
        self.blocks.append(vars(activity))


class Activity:
    """The activity block in the project section"""
    def __init__(self, name=None, description=None, icon=None,
                 link=None, slugs=None, **kwargs):
        self.name = name
        self.description = description
        self.icon = icon
        self.link = link
        self.slugs = slugs
