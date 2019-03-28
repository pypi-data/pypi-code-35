from .backend import get_backend
from .common import Color, Shape
import random
import math
from .config import Config

name = "sketcher"

config = Config()


class Sketch:
    def __init__(self):
        if not hasattr(self, 'Backend'):
            self.__Backend = get_backend()
        self._can = None

    def __start(self):
        self._can = self.__Backend()
        self._can.init()
        self._can.start(self.setup, self.loop)

    def clear(self):
        self._can.clear()

    def frame(self, l):
        self._can.set_frame(l)

    def fill(self):
        self._can.set_fill(True)

    def no_fill(self):
        self._can.set_fill(False)

    def stroke(self):
        self._can.set_stroke(True)

    def no_stroke(self):
        self._can.set_stroke(False)

    def fill_color(self, col):
        self._can.set_fill_color(col)

    def stroke_color(self, col):
        self._can.set_stroke_color(col)

    def mouse_state(self):
        return self._can.get_mouse_state()

    def keyboard_state(self, ):
        return self._can.get_keyboard_state()

    def size(self, w, h):
        self._can.set_size(w, h)

    def background(self, color):
        self._can.set_background(Color(color))

    def shape(self, shape):
        if not isinstance(shape, Shape):
            shape = Shape(list(shape))
        self._can.draw_shape(shape)

    def point(self, x, y):
        self._can.draw_point(x, y)

    def line(self, x1, y1, x2, y2):
        self._can.draw_line(x1, y1, x2, y2)

    def rectangle(self, x, y, w, h=None):
        if h is None:
            h = w
        self._can.draw_rectangle(x, y, w, h)

    def ellipse(self, x, y, a, b=None, angle=None, n=None):
        if b is None:
            b = a
        opts = {}
        if n:
            opts['n'] = n
        if angle:
            opts['angle'] = angle
        self._can.draw_ellipse(x, y, a, b, **opts)

    def text(self, x, y, text, **kwargs):
        self._can.draw_text(x, y, text, **kwargs)

    def image(self, x, y, image, anchor='center', scale=(1, 1)):
        self._can.draw_image(x, y, image, anchor, scale)

Sketch.m = math
Sketch.rd = random

try:
    import numpy
    Sketch.np = numpy
except ImportError:
    Sketch.np = None


def sketch(sk):
    if issubclass(sk, Sketch):
        MySketch = sk
    else:
        class MySketch(Sketch, sk):
            pass
    MySketch._Sketch__Backend = get_backend(config.backend_use)
    MySketch.__name__ = sk.__name__
    MySketch()._Sketch__start()
    return MySketch
