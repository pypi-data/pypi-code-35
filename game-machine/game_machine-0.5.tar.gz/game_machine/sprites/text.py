from .sprite import Sprite
import pygame

class Text(Sprite) :
    def __init__(self, coords, text, font_size = 32,
                 font = None, colour = (0, 0, 0, 255),
                 visible = True, interactive = True, transparency = True) :
        super(Text, self).__init__(coords, visible, interactive, transparency)
        self._text = text
        self._font_size = font_size
        self._font = font
        self._colour = colour
        self.__font_obj = pygame.font.SysFont(self._font, self._font_size)
        self.size = self.__font_obj.size(self._text)

    def create_surface(self) :
        self._surface = self.__font_obj.render(self._text, True, self._colour)

    def fill_surface(self) :
        if self._surface == None :
            self.create_surface()
        
    @property
    def text(self) :
        return self._text

    @property
    def font_size(self) :
        return self._font_size

    @property
    def font(self) :
        return self._font

    @text.setter
    def text(self, text) :
        self._text = text
        self._surface = None

    @font_size.setter
    def font_size(self, font_size) :
        self._font_size = font_size
        self.__font_obj = pygame.font.SysFont(self._font, self._font_size)
        self._surface = None

    @font.setter
    def font(self, font) :
        self._font = font
        self.__font_obj = pygame.font.SysFont(self._font, self._font_size)
        self._surface = None
