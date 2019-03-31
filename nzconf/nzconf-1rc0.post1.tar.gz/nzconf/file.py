import collections
import os,os.path
from pathlib2 import Path

_mode2access = collections.OrderedDict([
    ('r',os.R_OK),('w',os.W_OK),('x',os.X_OK)])
def mode2access(mode):
    access = 0
    for m in mode:
        access |= _mode2access.get(m.lower(),0)
    return access

def access2mode(access):
    mode = ''
    for m in _mode2access.keys():
        mode += m if (access & _mode2access[m]) else '-'
    return mode

class File(object):
    def __init__(self,filename=None,mode='r'):
        self.__filename = None if filename is None else Path(filename)
        self.__access   = self.check_mode(mode)
        self.__file     = None
        self.__io       = None

    @property
    def filename(self):
        if self.__filename is not None:
            return self.__filename

    @property
    def access(self):
        return int(self.__access)
    def check_mode(self,mode):
        wanted = mode2access(mode)
        if wanted & (os.R_OK|os.W_OK) != wanted:
            raise ValueError('check_mode() only supports read/write check')
        f = self.filename
        if f is None:
            return wanted
        d = f.absolute().parent
        if not d.exists():
            raise FileNotFoundError("No such directory: '%s'" % d)
        if not d.is_dir():
            raise TypeError("Not a directory: '%s'" % d)
        if not os.access(str(d),os.X_OK):
            raise PermissionError("Cannot enter directory: '%s'" % d)
        if f.exists():
            if not f.is_file():
                raise TypeError("Not a file: '%s'" % f)
            if not os.access(str(f),wanted):
                raise PermissionError(
                        "No '%s' rights: '%s'" % (access2mode(wanted),f))
            return wanted
        if (wanted & os.W_OK) and not os.access(str(d),os.W_OK):
            raise PermissionError("Directory not writable: '%s'" % d)
        return wanted

    @property
    def opened(self):
        return self.__file is not None

    @property
    def closed(self):
        return self.__io is None or self.__io.closed

    def open(self,mode):
        if not self.opened:
            access = mode2access(mode)
            if (access & self.access) != access:
                raise PermissionError(
                        "Permission denied. Requested %s, available %s." %
                        (access2mode(access),access2mode(self.access)))
            if self.filename is None:
                raise AttributeError('No filename specified.')
            try:
                self.__file = self.filename.open(mode)
            except FileNotFoundError as e:
                self.__file = open(os.devnull,mode)
        return self
    def close(self):
        if not self.closed:
            self.__io.close()
        self.__io = None
        self.__file = None

    def __enter__(self):
        if self.closed:
            assert self.opened
            self.__io = self.__file.__enter__()
        return self
    def __exit__(self,type,value,traceback):
        self.close()

    def writable(self,*args,**kwargs):
        return (not self.closed) and self.__io.writable(*args,**kwargs)
    def write(self,*args,**kwargs):
        return self.__io.write(*args,**kwargs)

    def readable(self,*args,**kwargs):
        return (not self.closed) and self.__io.readable(*args,**kwargs)
    def read(self,*args,**kwargs):
        return self.__io.read(*args,**kwargs)

    def __iter__(self):
        return iter(self.__io)

    def dump(self,*args,**kwargs):
        return self._dump(*args,**kwargs)
    def load(self,*args,**kwargs):
        return self._load(*args,**kwargs)

    def __str__(self):
        attributes = []
        if self.opened:
            attributes.append('opened')
        if self.closed:
            attributes.append('closed')
        if self.writable():
            attributes.append('writable')
        if self.readable():
            attributes.append('readable')
        attributes = ','.join(attributes)
        if attributes:
            attributes = ',' + attributes
        return "%s('%s',mode='%s'%s)" % (type(self).__name__,str(self.filename),access2mode(self.access),attributes)
