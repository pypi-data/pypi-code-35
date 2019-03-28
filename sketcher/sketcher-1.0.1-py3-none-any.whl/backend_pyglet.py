from .backend_base import CanvasBackend
from .common import KeyboardState, MouseState, Color, Ellipse
import pyglet as pg
from queue import Queue


def mouse_button(b):
    if b == pg.window.mouse.LEFT:
        return 1
    elif b == pg.window.mouse.RIGHT:
        return 3
    elif b == pg.window.mouse.MIDDLE:
        return 2
    else:
        return 0


def key_symbol(b):
    return pg.window.key.symbol_string(b).lower()


class Backend(CanvasBackend):
    def __init__(self):
        CanvasBackend.__init__(self)
        self.win = pg.window.Window(vsync=0)
        self.event_queue = Queue()
        self.size = (100, 100)

        self.stroke_color = Color('black')
        self.fill_color = Color('red')
        self.back_color = Color('white')
        self.batch = pg.graphics.Batch()
        self.redraw_back = True
        self.image_cache = {}
        self.sprites = []

        @self.win.event
        def on_key_press(symbol, modifiers):
            self.event_queue.put(('key_press', (symbol, modifiers)))

        @self.win.event
        def on_key_release(symbol, modifiers):
            self.event_queue.put(('key_release', (symbol, modifiers)))

        @self.win.event
        def on_mouse_press(x, y, button, modifiers):
            self.event_queue.put(('mouse_press', (x, y, button, modifiers)))

        @self.win.event
        def on_mouse_release(x, y, button, modifiers):
            self.event_queue.put(('mouse_release', (x, y, button, modifiers)))

        @self.win.event
        def on_mouse_motion(x, y, dx, dy):
            self.event_queue.put(('mouse_move', (x, y)))

        self.user_loop = None

        self.__keyboard_state = KeyboardState()
        self.__mouse_state = MouseState()

    def init(self):
        # setup background, canvas, focus
        pass

    def start(self, setup, loop):
        setup()
        self.user_loop = loop

        # run main loop
        self.loop()
        pg.app.run()

    def loop(self, dt=0):
        pg.clock.schedule_once(self.loop, self.frame)
        # poll event
        self.__mouse_state.clean()
        self.__keyboard_state.clean()

        while not self.event_queue.empty():
            # empty event list
            ev_type, ev = self.event_queue.get()
            if ev_type == 'key_press':
                self.__keyboard_state.pressed.add(key_symbol(ev[0]))
            elif ev_type == 'key_release':
                self.__keyboard_state.released.add(key_symbol(ev[0]))
            elif ev_type == 'mouse_move':
                self.__mouse_state.pos = (ev[0], ev[1])

            elif ev_type == 'mouse_press':
                self.__mouse_state.pressed.add(mouse_button(ev[2]))
                self.__mouse_state.pos = (ev[0], ev[1])

            elif ev_type == 'mouse_release':
                self.__mouse_state.released.add(mouse_button(ev[2]))
                self.__mouse_state.pos = (ev[0], ev[1])

        self.__mouse_state.clean()
        self.__keyboard_state.clean()

        self.win.clear()
        self.user_loop()
        if self.redraw_back:
            w, h = self.size
            back = pg.graphics.Batch()
            back.add(4, pg.gl.GL_QUADS, None,
                     ('v2i', (0, 0, w, 0, w, h, 0, h)),
                     ('c3B', self.back_color.tupple255()*4))
            back.draw()
            self.redraw_back = False
        self.batch.draw()

        self.sprites.clear()

    def clear(self):
        # clear canvas
        self.redraw_back = True
        self.batch = pg.graphics.Batch()

    def set_fill(self, yes):
        self.fill = yes

    def set_stroke(self, yes):
        self.stroke = yes

    def set_stroke_color(self, color):
        self.stroke_color = Color(color)

    def set_fill_color(self, color):
        self.fill_color = Color(color)

    def get_mouse_state(self):
        return self.__mouse_state

    def get_keyboard_state(self):
        return self.__keyboard_state

    def set_size(self, w, h):
        self.size = (w, h)
        self.win.set_size(w, h)

    def set_background(self, color):
        # set background color
        self.back_color = color
        self.redraw_back = True

    def draw_point(self, x, y):
        self.batch.add(1, pg.gl.GL_POINTS, None,
                       ('v2f', (float(x), float(y))),
                       ('c3B', self.stroke_color.tupple255()))

    def draw_line(self, x1, y1, x2, y2):
        self.batch.add(2, pg.gl.GL_LINES, None,
                       ('v2f', (x1, y1, x2, y2)),
                       ('c3B', self.stroke_color.tupple255()*2))

    def draw_rectangle(self, x, y, w, h):
        x0, y0 = float(x), float(y)
        x1, y1 = float(x+w), float(y+h)
        if self.fill:
            self.batch.add(4, pg.gl.GL_QUADS, None,
                           ('v2f', (x0, y0, x1, y0, x1, y1, x0, y1)),
                           ('c3B', self.fill_color.tupple255()*4))
        if self.stroke:
            self.draw_line(x0, y0, x1, y0)
            self.draw_line(x1, y0, x1, y1)
            self.draw_line(x1, y1, x0, y1)
            self.draw_line(x0, y1, x0, y0)

    def draw_ellipse(self, x, y, a, b=0, anlge=0, n=0):
        self.draw_shape(Ellipse(x, y, a, b, angle=0, n=n))

    def draw_text(self, x, y, text, **kwargs):
        opts = {}
        if 'font' in kwargs:
            opts['font_name'] = kwargs['font']
        if 'size' in kwargs:
            opts['font_size'] = kwargs['size']

        if 'color' in kwargs:
            opts['color'] = Color(kwargs['color']).tupple255alpha()
        else:
            opts['color'] = (0, 0, 0, 255)

        pg.text.Label(text, batch=self.batch, x=x, y=y, **opts)

    def draw_shape(self, shape):
        if self.fill:
            vtx = []
            for tri in shape.to_tris():
                for v in tri:
                    vtx.extend(v)
            n = len(vtx)//2
            self.batch.add(n, pg.gl.GL_TRIANGLES, None,
                           ('v2f', vtx),
                           ('c3B', self.fill_color.tupple255()*n))
        if self.stroke:
            vtx = []
            for i in range(len(shape.vertex)):
                if i == len(shape.vertex)-1:
                    self.draw_line(*shape.vertex[i], *shape.vertex[0])
                else:
                    self.draw_line(*shape.vertex[i], *shape.vertex[i+1])

    def draw_image(self, x, y, filename, anchor='center', scale=(1, 1)):
        if filename not in self.image_cache:
            self.image_cache[filename] = pg.image.load(filename)
        img = self.image_cache[filename]
        if anchor == 'center' or anchor == 'n' or anchor == 's':
            img.anchor_x == img.width//2
        elif 'w' in anchor:
            img.anchor_x = 0
        else:
            img.anchor_x = img.width

        if anchor == 'center' or anchor == 'w' or anchor == 'e':
            img.anchor_y == img.width//2
        elif 's' in anchor:
            img.anchor_y = 0
        else:
            img.anchor_y = img.width

        sp = pg.sprite.Sprite(img, batch=self.batch)
        sp.update(x, y, scale_x=scale[0], scale_y=scale[1])
        self.sprites.append(sp)
