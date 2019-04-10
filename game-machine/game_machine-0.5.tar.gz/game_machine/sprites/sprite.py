import pygame
import math

from ..eventobject import EventObject

class Sprite(EventObject) :
    def __init__(self, \
                 coords, \
                 visible = True, \
                 interactive = True, \
                 transparency = True) :
        super(Sprite, self).__init__()
        self.coords = coords
        self.visible = visible
        self.interactive = interactive
        self.transparency = transparency
        self.size = None
        self._margin = 0
        self.__over = False
        self.__rotation = None
        self._screen = None
        self._surface = None
        self._surface_pos_override = None

    def create_surface(self) :
        if self.transparency :
            self._surface = pygame.Surface((self.width + (self._margin * 2),
                                             self.height + (self._margin * 2)),
                                           pygame.SRCALPHA, 32)
        else :
            self._surface = pygame.Surface((self.width + (self._margin * 2),
                                             self.height + (self._margin * 2)))
    def fill_surface(self) :
        if self._surface == None :
            self.create_surface()
        if self.transparency :
            self._surface.fill((self._screen.colour[0], \
                                self._screen.colour[1], \
                                self._screen.colour[2], 0))
##            self._surface.fill((255, 0, 0))
        else :
            self._surface.fill(self._screen.colour)
    
    def place_surface(self) :
        if self._screen != None :
            if self._surface_pos_override == None :
	            self._screen.pygame_screen.blit(self._surface, \
                        self._screen.to_pygame_coords(self.coords, self.size_margin, self._margin))
            else :
	            self._screen.pygame_screen.blit(self._surface, self._surface_pos_override)
            

    def update(self) :
        if self.interactive and self._screen != None :
            mouse_pos = self._screen.get_mouse_coords()
            if self.over(mouse_pos):
                self.trigger('mouse_over', None)
                if not self.__over:
                    self.trigger('mouse_enter', None)
                self.__over = True
                evs = self._screen.pygame_events
                if evs != None :
                    for ev in evs :
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            self.trigger('click', None)
            else:
                if self.__over:
                    self.trigger('mouse_leave', None)
                self.__over = False

    def bounds(self) :
        if self.size == None :
            return (self.coords, self.coords)
        elif self._screen.cartesian :
            return ((self.coords[0] - (self.size[0] / 2),
                     (self.coords[1] + (self.size[1] / 2))),
                    (self.coords[0] + (self.size[0] / 2),
                     (self.coords[1] - (self.size[1] / 2))))
        else :
            return (self.coords,
                    (self.coords[0] + self.size[0],
                     self.coords[1] + self.size[1]))
            
       
    def in_bounds(self, coords) :
        if coords == None :
            return False
        else :
            bounds = self.bounds()
            if self._screen.cartesian :
                return bounds[0][0] <= coords[0] and \
                       coords[0] <= bounds[1][0] and \
                       bounds[0][1] >= coords[1] and \
                       coords[1] >= bounds[1][1]
            else :
                return bounds[0][0] <= coords[0] and \
                       coords[0] <= bounds[1][0] and \
                       bounds[0][1] <= coords[1] and \
                       coords[1] <= bounds[1][1]

    def over(self, coords) :
        return self.in_bounds(coords)

    def bounds_intersect(self, other_sprite) :
        self_bounds = self.bounds()
        other_sprite_bounds = other_sprite.bounds()
        if self._screen.cartesian :
            return not(other_sprite_bounds[0][0] > self_bounds[1][0] or \
                       other_sprite_bounds[1][0] < self_bounds[0][0] or \
                       other_sprite_bounds[0][1] < self_bounds[1][1] or \
                       other_sprite_bounds[1][1] > self_bounds[0][1])
        else :
            return not(other_sprite_bounds[0][0] > self_bounds[1][0] or \
                       other_sprite_bounds[1][0] < self_bounds[0][0] or \
                       other_sprite_bounds[0][1] > self_bounds[1][1] or \
                       other_sprite_bounds[1][1] < self_bounds[0][1])

    def is_on_screen(self) :
        return self.bounds_intersect(self._screen)
    
    def draw(self) :
        if self.visible and self._screen != None :
            self._draw()
            
    def _draw(self) :
        if self._surface == None :
            self.fill_surface()
        self.place_surface()        

    @property
    def coords(self) :
         return self._coords

    @coords.setter
    def coords(self, coords) :
         self._coords = coords

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, x):
        self.coords = (x, self.coords[1])
        
    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, y):
        self.coords = (self.coords[0], y)
        
    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, r):
        self.__rotation = r
        self.__rotation %= 360

    @property
    def width(self):
        return self.size[0] if self.size != None else 0
    @property
    def height(self):
        return self.size[1] if self.size != None else 0

    @property
    def size_margin(self):
        size = self.size if self.size != None else (0, 0)
        return (size[0] + (self._margin * 2), size[1] + (self._margin * 2))

    @property
    def top(self) :
        bounds = self.bounds()
        return bounds[0][1]

    @top.setter
    def top(self, top) :
        self.y = top - self.height / 2.0

    @property
    def bottom(self) :
        bounds = self.bounds()
        return bounds[1][1]

    @bottom.setter
    def bottom(self, bottom) :
        self.y = math.floor(bottom + self.height / 2.0)

    @property
    def left(self) :
        bounds = self.bounds()
        return bounds[0][0]

    @left.setter
    def left(self, left) :
        self.x = left + self.width / 2.0

    @property
    def right(self) :
        bounds = self.bounds()
        return bounds[1][0]

    @right.setter
    def right(self, right) :
        self.x = right - self.width / 2.0
