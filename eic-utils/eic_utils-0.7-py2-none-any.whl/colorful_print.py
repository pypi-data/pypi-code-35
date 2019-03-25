__normalize = lambda x: max(0, min(5, int(x / 256 * 6)))
def __color(rgb, s=None):
    r, g, b = map(__normalize, rgb)
    code = r * 6 * 6 + b * 6 + g + 16
    if s is not None: return "\033[38;5;{}m{}\033[m".format(code, s)
    return "\033[48;5;{}m  \033[m".format(code)

def img_to_str(img, w, h):
    rate = np.min(np.array([h, w]) / img.shape[:2])
    h, w = np.round(np.array(img.shape[:2]) * rate).astype(int)
    img = cv2.resize(img, (w, h))
    s = ''
    for i in range(img.shape[0]):
        s += ''.join(map(__color, img[i])) + '\n'
    return s

class ColorfulPrint(object):# {{{

    """Docstring for ColorfulPrint. """

    def __init__(self):
        """nothing needs to be define """
        self.colors = {
            'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
            'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37,
            'b': 34, 'r': 31, 'g': 32, 'y': 33, 'w': 37,
        }
        self.done = '(#g)done(#)'

    def trans(self, *args, auto_end=True):
        s = ' '.join(map('{}'.format, args))
        s = s.replace('(##)', '\033[0m')
        s = s.replace('(#)', '\033[0m')
        for color, value in self.colors.items():
            color_tag = '(#%s)'%color
            s = s.replace(color_tag, '\033[%dm'%value)
        if auto_end:
            s = s + '\033[0m'
        return s

    def err(self, *args, **kwargs):
        return self('(#r)[ERR](#)', *args, **kwargs)

    def log(self, *args, **kwargs):
        return self('(#b)[LOG](#)', *args, **kwargs)

    def wrn(self, *args, **kwargs):
        return self('(#y)[WRN](#)', *args, **kwargs)

    def suc(self, *args, **kwargs):
        return self('(#g)[SUC](#)', *args, **kwargs)

    def __call__(self, *args, **kwargs):
        print(self.trans(*args), **kwargs)

cp = ColorfulPrint()
# }}}
