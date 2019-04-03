"""
MIT License

Copyright (c) 2019 Andre Augusto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class Syntatic:
    def __init__(self, prefix=None, suffix=None, both=True, 
                 strip_inside=(True, True), strip_outside=(True,True)):
        self.prefix = prefix
        self.suffix = suffix
        self.both = both
        self.strip_inside = strip_inside
        self.strip_outside = strip_outside
    
    def __call__(self, ktx):
        c = ktx._message.content
        s = c.lstrip() if self.strip_outside[0] else c
        e = c.rstrip() if self.strip_outside[1] else c
        s = self.prefix is None or s.startswith(self.prefix)
        e = self.suffix is None or e.endswith(self.suffix)
        if (s and e if self.both else s or e):
            if s and self.prefix is not None:
                cut = c.find(self.prefix) + len(self.prefix)
                c = c[cut:]
                if self.strip_inside[0]:
                    c = c.lstrip()
            if e and self.suffix is not None:
                cut = c.rfind(self.suffix)
                c = c[:cut]
                if self.strip_inside[1]:
                    c = c.rstrip()
            ktx._message.content = c
            return True
        return False

class Mentioning:
    def __init__(self, user, strip=True):
        self.user = user
        self.strip = True

    def __call__(self, ktx):
        c = ktx._message.content
        if self.user in ktx._message.mentions:
            c = c.replace(self.user.mention, '')
            c = c.replace(self.user.mention.replace('<@', '<@!'), '')
            ktx._message.content = c.strip() if self.strip else c
            return True
        return False
