

from .memzero import memzero

class SecureString(str):
    '''When garbage collected, leaves behind only a string of zeroes.'''

    def __init__(self, anystring):
        self._string = anystring

    def burn(self):
        memzero(self._string)
    
    def __del__(self):
        #print("I'm being deleted!")
        memzero(self._string)

    def __str__(self):
        return self._string
        
    def __repr__(self):
        return self._string

