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
    def __init__(self, name=None, description=None, slugs=None, flair=None,
                 flair_icon=None, flair_link=None, **kwargs):
        self.name = name
        self.flair = flair
        self.flair_icon = flair_icon
        self.flair_link = flair_link
        self.description = description
        self.slugs = slugs
