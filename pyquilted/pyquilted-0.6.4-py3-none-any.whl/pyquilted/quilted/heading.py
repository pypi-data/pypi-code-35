class Heading:
    """The heading section located at the top of a quilted resume

       A simple heading format that is centered. Has name, title and location.
    """
    def __init__(self, name="", title="", location="", via="", **kwargs):
        self.name = name
        self.title = title
        self.location = location
        self.via = "fa-" + via

    def serialize(self):
        return vars(self)
