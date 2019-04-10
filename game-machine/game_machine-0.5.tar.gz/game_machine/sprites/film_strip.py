from .sprite import Sprite
import pygame
import math

class FilmStrip(Sprite) :
    
    def __init__(self,
                 image_file,
                 aperture,
                 no_of_frames = None,
                 frame = 0,
                 coords = (0, 0),
                 visible = True,
                 interactive = True,
                 transparency = True,
                 stop_frames = []) :
        
        super(FilmStrip, self).__init__(coords, visible, \
                                        interactive, transparency)
        self.size = aperture
        self._image = pygame.image.load(image_file)
        if transparency :
            self._image = self._image.convert_alpha()

        self.__image_size = self._image.get_width(), self._image.get_height()
        self.__image_centre = self.__image_size[0] / 2, self.__image_size[1] / 2
        self._fw = int(self._image.get_width() / self.size[0])
        self._fh = int(self._image.get_height() / self.size[1])
        if no_of_frames == None :
            self.no_of_frames = int(self._fw * self._fh)
        else :
            self.no_of_frames = no_of_frames
        self._frame = frame
        self._frames_pos = [(-(f % self._fw) * self.size[0],
                             -int(f / self._fw) * self.size[1])
                            for f in range(self.no_of_frames)]
        self._fill_needed = True
        self.stop_frames = stop_frames

    def fill_surface(self) :
        super(FilmStrip, self).fill_surface()
        self._surface.blit(self._image, self._frames_pos[self._frame])
        self._fill_needed = False

    def _draw(self) :
        if self._surface == None or self._fill_needed :
            self.fill_surface()
        self.place_surface()        

##    def _draw(self, screen) :
##        frame_image = pygame.Surface(self.aperture)
##        offset = ((self.frame % self._fw) * self.aperture[0],
##                  (self.frame % self._fh) * self.aperture[1])
##        frame_image.blit(self.image, (0, 0), pygame.Rect(offset, self.aperture))
##        if self.rotation is not None:
##            frame_image = pygame.transform.rotate(frame_image, self.rotation)
##        screen_co_ords = screen.cartesian(self.co_ords, self.aperture)
##        screen_co_ords = (screen_co_ords[0] - ((frame_image.get_width() -
##                                                self.aperture[0]) / 2),
##                          screen_co_ords[1] - ((frame_image.get_height() -
##                                                self.aperture[1]) / 2))
##        
##        screen.pygame_screen.blit(frame_image, screen_co_ords)
        
    def update(self) :
        super(FilmStrip, self).update()
        if not self.frame in self.stop_frames :
            self.advance()
            
    def advance(self, by = 1) :
        self.frame += by
        self.frame = self.frame % self.no_of_frames
        

    @property
    def frame(self) :
        return self._frame

    @frame.setter
    def frame(self, frame) :
        old_frame = self._frame
        self._frame = int(frame)
        self._fill_needed = True
        if frame != old_frame :
            self.trigger('frame_change',
                         {'old_frame': old_frame, 'new_frame': frame})
        

