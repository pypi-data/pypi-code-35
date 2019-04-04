from pyquilted.quilted.iconify import Iconify


class Detail:
    def serialize(self):
        name = self.__class__.__name__ + '-detail'
        detail = dict()
        detail[name.lower()] = vars(self)
        return detail


class Location(Detail, Iconify):
    def __init__(self, location=None, via=None, **kwargs):
        self.location = location
        self.via = self.iconify(value=via)


class Flair(Detail):
    def __init__(self, flair=None, flair_icon=None, flair_link=None, **kwargs):
        self.flair = flair
        self.icon = flair_icon
        self.link = flair_link


class Objective(Detail):
    def __init__(self, objective=None, **kwargs):
        self.objective = objective


class Title(Detail):
    def __init__(self, title=None, **kwargs):
        self.title = title
