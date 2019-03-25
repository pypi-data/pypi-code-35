"""
Summary:
    Color code shortcut mapping class library

Module Classes:
    :ColorEntity:  Packaging class for single color code & assoc attributes
    :ColorMap:  Builds map of ColorEntity objects indexed by shortcut names
    :ColorMapper:  Wrapper class for ColorMap; calling class for entire chain

"""

from pyaws import Colors

# color object
co = Colors()


class ColorEntity():
    def __init__(self, name, hexcode, description=''):
        self.name = name
        self.code = hexcode
        self.description = description

    def __repr__(self):
        """Returns a hexcode str if printed"""
        return self.code


class ColorMap():
    """
    Class providing color index based on short attribute names
    """
    def __init__(self):
        """
        Color shortcuts defined here as class attributes
        """
        self.act = co.ORANGE
        self.accent = co.ORANGE
        self.aqu = co.AQUA
        self.bbc = co.BOLD + co.BRIGHTCYAN
        self.bd = co.BOLD
        self.bbl = co.BRIGHTBLUE
        self.bgn = co.BRIGHTGREEN
        self.borg = co.BOLD + co.ORANGE
        self.bpl = co.BRIGHTPURPLE
        self.bwt = co.BRIGHTWHITE
        self.bdwt = co.BOLD + co.BRIGHTWHITE
        self.btext = co.BOLD + co.BRIGHTCYAN
        self.byl = co.BOLD + co.BRIGHTYELLOW
        self.byg = co.BRIGHTYELLOWGREEN
        self.dbl = co.DARKBLUE
        self.dcy = co.DARKCYAN
        self.dg1 = co.DARKGRAY1
        self.dg2 = co.DARKGRAY2
        self.highlight = co.BRIGHTYELLOW2
        self.fs = co.GOLD3
        self.filesysystem = co.GOLD3
        self.gray = co.LT2GRAY
        self.text = co.BRIGHTCYAN
        self.frame = co.BRIGHTGREEN
        self.org = co.ORANGE
        self.rd = co.RED
        self.ub = co.UNBOLD
        self.wtgr = co.WHITEGRAY
        self.yl = co.YELLOW
        self.rst = co.RESET
        #self.colormap = self.map()

    def code(self, color):
        return getattr(self, color)

    def run(self, color):
        return getattr(self, color)

    def search(self, color):
        """
        Returns:
            all attribute names matching search color, TYPE: list
        """
        return [x for x in dir(self) if (color in x) and (not x.startswith('__'))]

    def contents(self):
        """
        Returns the index; list of all color shortcuts, TYPE: list
        """
        return [{x: getattr(self, x)} for x in dir(self) if not x.startswith('__')]


class ColorAttributes():
    def __init__(self):
        self.cm = ColorMap()
        self.map = self.mapper()

    def mapper(self):
        """
        Summary:
            Use map method when attribute name is uncertain
        Returns:
            :attribute (hex code, TYPE: str)
        """
        m = {}
        for d in [{k: v} for k, v in type(co).__dict__.items() if not k.startswith('__')]:
            for hex_dict in [{x: getattr(self.cm, x)} for x in dir(self.cm) if not x.startswith('__')]:
                for k, v in d.items():
                    for hex_k, hex_v in hex_dict.items():
                        if hex_v == v:
                            m[hex_k] = ColorEntity(name=hex_k, hexcode=v, description=k)
        return m

    def describe(self, color):
        return self.map.get(color).description if self.map.get(color) else None

    def hex(self, color):
        return self.map.get(color).code

    def contents(self):
        """
        Prints out color names highlighted in respective color codes
        """
        tab4 = '\t'.expandtabs(4)
        tab8 = '\t'.expandtabs(8)
        print('\n{}Color Names:'.format(tab4))
        return [print('{}{}{}'.format(tab8, v, k)) for k, v in self.map.items()][0]
