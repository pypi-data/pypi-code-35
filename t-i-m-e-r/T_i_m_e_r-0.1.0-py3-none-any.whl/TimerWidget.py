import time
import math
import functools

import tkinter as tk
import tkinter.font as tfont

from .lib.ConfMixin import ConfMixin
from .lib.misc import fit_text, duration2hms


class TimerWidget(ConfMixin):
    NEW = 0
    RUNNING = 1
    STOPPED = 2
    EXPIRED = 3

    NORMAL = 0
    ACTIVE = 1

    _BG = {NORMAL: '#FFF', ACTIVE: '#EEE'}

    def __init__(self, master, *, name='', duration=0):
        ConfMixin.__init__(self)

        self._d = {}
        self._d['name'] = name
        self._d['duration'] = duration
        self._d['gone'] = 0
        self._d['status'] = self.NEW

        self._t0 = 0
        self._state = None

        self.frame = tk.Frame(master, borderwidth=0, highlightthickness=0)
        self.frame.bind('<Configure>', self._onresize)

        self._canvas = tk.Canvas(self.frame, borderwidth=0, highlightthickness=0)
        self._canvas.grid(row=0, column=0, rowspan=2)

        self._font1 = tfont.Font(font='Courier')
        self._label1 = tk.Label(self.frame, font=self._font1, anchor=tk.CENTER, justify=tk.CENTER, foreground='#000')
        self._label1.grid(row=0, column=1, sticky=tk.NSEW)

        self._font2 = tfont.Font(font='Courier')
        self._label2 = tk.Label(self.frame, font=self._font2, anchor=tk.CENTER, justify=tk.CENTER, foreground='#666')
        self._label2.grid(row=1, column=1, sticky=tk.NSEW)

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=3, uniform='a')
        self.frame.rowconfigure(1, weight=1, uniform='a')

        self.frame.grid_propagate(False)  # to avoid possible resizing feedback

        self._canvas.bind('<ButtonRelease-1>', self._canvas_onclick)

        self._set_state(self.NORMAL)

        self._register_conf(name='name', func_get=lambda : self._d['name'], func_set=lambda _: self._d.__setitem__('name', _))
        self._register_conf(name='duration', func_get=lambda : self._d['duration'])
        self._register_conf(name='state', func_get=lambda : self._state, func_set=lambda _: self._set_state(_))

    def _set_state(self, state):
        if state == self._state:
            return
        self._state = state

        for _ in [self._canvas, self._label1, self._label2]:
            _['background'] = self._BG[self._state]

    def status(self):
        return self._d['status']

    def save(self):
        d = dict(self._d)
        if d['status'] == self.RUNNING:
            d['status'] = self.STOPPED
        return d

    def restore(self, d):
        self._d = dict(d)
        self._draw()

    def configure(self, **kwargs):
        res = ConfMixin.configure(self, **kwargs)
        if len(kwargs) > 0:
            self._draw()
        return res

    def tick(self):
        if self._d['status'] != self.RUNNING:
            return

        self._t0, t0 = time.time(), self._t0
        self._d['gone'] += self._t0 - t0
        if self._d['gone'] >= self._d['duration']:
            self._d['gone'] = self._d['duration']
            self._d['status'] = self.EXPIRED

        self._draw()

    def start(self):
        if self._d['status'] == self.RUNNING:
            return

        if self._d['status'] in [self.NEW, self.EXPIRED]:
            self._d['gone'] = 0

        self._t0 = time.time()
        self._d['status'] = self.RUNNING
        self.tick()

    def restart(self):
        self._d['status'] = self.NEW
        self.start()

    def stop(self):
        assert self._d['status'] == self.RUNNING

        self._d['status'] = self.STOPPED
        self._draw()

    def _draw(self):
        h = self.frame.winfo_height()

        x1, y1, x2, y2 = 0.1 * h, 0.1 * h, 0.9 * h, 0.9 * h
        width = 0.1 * h
        self._canvas.delete(tk.ALL)
        if self._d['status'] == self.EXPIRED:
            self._canvas.create_oval(x1, y1, x2, y2, outline='#CCCCCC', width=width)
        elif self._d['status'] == self.NEW:
            self._canvas.create_oval(x1, y1, x2, y2, outline='#2981CC', width=width)
        else:
            arc_gone = int(self._d['gone'] * 360 / self._d['duration'])
            if arc_gone == 0:
                self._canvas.create_oval(x1, y1, x2, y2, outline='#2981CC', width=width)
            else:
                self._canvas.create_arc(x1, y1, x2, y2, outline='#2981CC', width=width, style=tk.ARC, start=90+arc_gone, extent=360-arc_gone)
                self._canvas.create_arc(x1, y1, x2, y2, outline='#CCCCCC', width=width, style=tk.ARC, start=90, extent=arc_gone)

        r = 0.25 * h
        ox, oy = 0.5 * h, 0.5 * h

        def _draw_icon_start():
            self._canvas.create_polygon(ox + r, oy, ox - 0.5 * r, oy - 0.866 * r, ox - 0.5 * r, oy + 0.866 * r, fill='#000')

        def _draw_icon_stop():
            self._canvas.create_rectangle(ox - 0.707 * r, oy - 0.707 * r, ox + 0.707 * r, oy + 0.707 * r, width=0, fill='#000')

        if self._d['status'] == self.RUNNING:
            _draw_icon_stop()
        else:
            _draw_icon_start()

        def _format_time(n):
            return '%02d:%02d:%02d' % duration2hms(n)

        w = self.frame.winfo_width() - h
        self._label1['text'] = fit_text(_format_time(int(self._d['duration'] - self._d['gone'])), self._font1, w, ellipsis=False)
        self._label2['text'] = fit_text('%s - %s' % (_format_time(int(self._d['duration'])), self._d['name']), self._font2, w)

    def _canvas_onclick(self, e):
        h = self.frame.winfo_height()
        r = 0.35 * h
        x, y = e.x, e.y

        if math.pow((x - 0.5 * h), 2) + math.pow((y - 0.5 * h), 2) < r * r:
            if self._d['status'] == self.RUNNING:
                self.stop()
            else:
                self.start()

    def _onresize(self, _):
        h = self.frame.winfo_height()

        self._canvas['width'] = h
        self._canvas['height'] = h

        self._font1['size'] = h * 3 // 8
        self._font2['size'] = h // 8

        self._draw()

    def bind(self, *args, **kwargs):
        for _ in [self._canvas, self._label1, self._label2]:
            _.bind(*args, **kwargs)

    def unbind(self, *args, **kwargs):
        for _ in [self._canvas, self._label1, self._label2]:
            _.unbind(*args, **kwargs)

    @classmethod
    def min_width(cls, height):
        return height + tfont.Font(font=('Courier', height * 3 // 8)).measure('00:00:00') + 8
