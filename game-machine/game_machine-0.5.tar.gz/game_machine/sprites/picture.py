from .sprite import Sprite
import pygame
import math

class Picture (Sprite) :
    
    def __init__(self,
                 image_file,
                 co_ords = (0, 0),
                 visible = True,
                 interactive = True,
                 transparency = True) :

        super(Picture, self).__init__(co_ords, visible, interactive, transparency)
        self._surface = pygame.image.load(image_file)
        if transparency :
            self._surface = self._surface.convert_alpha()
        self.size = self._surface.get_width(), self._surface.get_height()
