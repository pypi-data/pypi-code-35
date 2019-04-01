import os

_formats = [f[:-3] for f in os.listdir(os.path.curdir) if f.endswith('.py') and not f.startswith('__')]
