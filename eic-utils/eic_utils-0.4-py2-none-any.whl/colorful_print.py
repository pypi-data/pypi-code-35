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
