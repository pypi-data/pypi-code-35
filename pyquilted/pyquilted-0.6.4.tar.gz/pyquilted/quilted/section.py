import re


class Section:
    """A mixin class that contains the serialize method for a section"""
    def serialize(self):
        section = dict()
        section[self._kebab_name()] = vars(self)
        return section

    def _kebab_name(self):
        matches= re.findall('[A-Z][^A-Z]*', str(self.__class__.__name__))
        name = '-'.join(matches).lower()
        return name
