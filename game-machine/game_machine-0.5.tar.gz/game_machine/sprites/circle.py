from .vector_sprite import VectorSprite
from math import sqrt
import pygame

class Circle(VectorSprite) :
    def __init__(self, coords, radius,
                 visible = True, interactive = True,
                 line_colour = (0, 0, 0, 255),
                 line_width = 1,
                 fill_colour = (255, 255, 255, 255)):
        super(Circle, self).__init__(coords, visible, interactive,
                                     line_colour, line_width, fill_colour)
        self.radius = radius
        self._radius = radius + int(self.line_width / 2)
        self.size = (self._radius * 2, self._radius * 2)

    def over(self, coords) :
        if coords != None and self.in_bounds(coords) :
            dist = sqrt((coords[0] - self.x)**2 + (coords[1] - self.y)**2)
            return dist <= self._radius

    def fill_surface(self) :
        super(Circle, self).fill_surface()
        if self._fill_colour != None :
            pygame.draw.circle(self._surface, self._fill_colour, \
                               (int(self._radius), int(self._radius)),
                               self.radius, 0)
        if self.line_width > 0 :
            pygame.draw.circle(self._surface, self._line_colour, \
                               (self._radius, self._radius), \
                               self._radius, self._line_width)
