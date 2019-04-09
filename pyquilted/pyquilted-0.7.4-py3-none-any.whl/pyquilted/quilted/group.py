from pyquilted.quilted.section import Section


class Group(Section):
    """The group section in a quilted resume

       The group object is a meta section that represents a group
       of consecutive compact sections that will appear closer
       together in one div.
    """
    def __init__(self):
        self.blocks = []
        self.last = None

    def add_section(self, section):
        self.last = section
        first = list(section.keys())[0]
        self.blocks.append(section[first])

    def get_sections(self):
        if len(self.blocks) == 1:
            return self.last
        else:
            return self.serialize()
