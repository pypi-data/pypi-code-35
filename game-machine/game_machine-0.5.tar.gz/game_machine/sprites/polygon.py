from .vector_sprite import VectorSprite
##from math import abs
import pygame

class Polygon(VectorSprite):
    def __init__(self, co_ords, outline,
                 visible = True, interactive = True,
                 line_colour = (0, 0, 0, 1),
                 line_width = 1,
                 fill_colour = (255, 255, 255, 1)):
        self._min_x = self._max_x = self._min_y = self._max_y = 0
        self._screen = None   
        super(Polygon, self).__init__(co_ords, visible, interactive,
                                     line_colour, line_width, fill_colour)
        self._outline = []
        self.outline = outline

    def fill_surface(self) :
        super(Polygon, self).fill_surface()
        outline = [(x - self._min_x, -y + self._max_y) for (x, y) in self.outline]
        self._surface_pos_override = self._screen.to_pygame_coords(self.coords)
        self._surface_pos_override = (self._surface_pos_override[0] + self._min_x, \
                                      self._surface_pos_override[1] - self._max_y)
        pygame.draw.polygon(self._surface, self.line_colour,
                            outline, self.line_width)

    @property
    def outline(self) :
        return self._outline

    @outline.setter
    def outline(self, outline) :
        self._max_x = self._min_x = outline[0][0]
        self._max_y = self._min_y = outline[0][1]
        for line in outline:
            if line[0] > self._max_x:
                self._max_x = line[0]
            if line[0] < self._min_x:
                self._min_x = line[0]
            if line[1] > self._max_y:
                self._max_y = line[1]
            if line[1] < self._min_y:
                self._min_y = line[1]
        self.bounding_box = ((self._min_x, self._min_y), (self._max_x, self._max_y))
        self.size = ((self._max_x - self._min_x) + 1, (self._max_y - self._min_y) + 1)
        self._outline = outline
        self._surface = None

    @property
    def coords(self) :
         return self._coords


    @coords.setter
    def coords(self, coords) :
         self._coords = coords
         if self._screen != None :
             self._surface_pos_override = self._screen.to_pygame_coords(self.coords)
             self._surface_pos_override = (self._surface_pos_override[0] + self._min_x, \
                                      self._surface_pos_override[1] - self._max_y)
    