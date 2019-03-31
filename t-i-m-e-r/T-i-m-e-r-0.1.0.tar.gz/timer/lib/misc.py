import random
import enum
import re


def _fit_text(s1, s2, font, width, n):
    if font.measure(s1) <= width:
        if n <= 1:
            return s1
    else:
        s1, s2 = s1[:-n], s1[-n:] + s2

    n = min(n // 2, len(s2))
    s1, s2 = s1 + s2[:n], s2[n:]

    return _fit_text(s1, s2, font, width, n)


def fit_text(s, font, width, ellipsis=True):
    if font.measure(s) <= width:
        return s

    if ellipsis:
        _ = font.measure('...')
        return '' if _ > width else _fit_text(s, '', font, width - _, len(s)) + '...'

    return _fit_text(s, '', font, width, len(s))


def lorem(n=6, s=''.join([chr(ord(_1) + _2) for _1 in ['a', 'A'] for _2 in range(26)])):
    return ''.join([random.choice(s) for _ in range(n)])


def duration2hms(n):
    assert n >= 0

    n_sec = n % 60
    n_min = (n // 60) % 60
    n_hour = n // 3600

    assert n_hour < 100

    return (n_hour, n_min, n_sec)


def hms2duration(n_hour, n_min, n_sec):
    return n_hour * 3600 + n_min * 60 + n_sec


def center_window(win, *, _v={}):
    master = win.master
    if master is not None:
        x1, y1, w1, h1 = master.winfo_rootx() + _v.get('dx', 0), master.winfo_rooty() + _v.get('dy', 0), master.winfo_width(), master.winfo_height()
    else:
        # @win is the root window, i.e. its master is the screen
        x1, y1, w1, h1 = 0, 0, win.winfo_screenwidth(), win.winfo_screenheight()

    w2, h2 = win.winfo_width(), win.winfo_height()
    x2, y2 = x1 + (w1 - w2) // 2, y1 + (h1 - h2) // 2
    win.geometry('+%d+%d' % (x2, y2))

    if _v.get('dx') is None:
        x1, y1 = win.winfo_rootx(), win.winfo_rooty()

        win.geometry('+%d+%d' % (x1, y1))
        win.update()

        x2, y2 = win.winfo_rootx(), win.winfo_rooty()
        _v['dx'], _v['dy'] = x1 - x2, y1 - y2

        center_window(win)


class WindowingSystem(enum.Enum):
    X11 = enum.auto()
    WIN32 = enum.auto()
    AQUA = enum.auto()

    @classmethod
    def windowingsystem(cls, win, *, _v={'res': None}):
        if _v['res'] is None:
            _d = {
                'x11': cls.X11,
                'win32': cls.WIN32,
                'aqua': cls.AQUA
            }
            x = win.tk.call('tk', 'windowingsystem')
            if x in _d:
                _v['res'] = _d[x]
            else:
                raise RuntimeError('Unknown windowing system: %s' % x)

        return _v['res']
