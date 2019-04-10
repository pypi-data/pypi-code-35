from .sprite import Sprite

class VectorSprite(Sprite) :
    def __init__(self, co_ords, visible = True, interactive = True,
                 line_colour = (0, 0, 0, 1),
                 line_width = 1,
                 fill_colour = (255, 255, 255, 1)):
        super(VectorSprite, self).__init__(co_ords, visible, interactive)
        self._line_colour = line_colour
        self._line_width = line_width
        self._fill_colour = fill_colour

    @property
    def line_colour(self) :
        return self._line_colour

    @line_colour.setter
    def line_colour(self, colour) :
        self._line_colour = colour
        self._surface = None

    @property
    def line_width(self) :
        return self._line_width

    @line_width.setter
    def line_width(self, line_width) :
        self._line_width = int(line_width)
        self._surface = None

    @property
    def fill_colour(self) :
        return self._fill_colour

    @fill_colour.setter
    def fill_colour(self, fill_colour) :
        self._fill_colour = fill_colour
        self._surface = None
