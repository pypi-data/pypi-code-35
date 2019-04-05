'''
0.0.8 add text search template
0.0.9 update service template url; auto check version
'''
name = 'm2c'
version = '0.0.9'

def check_version():
    import os
    from .conf import Color
    text = os.popen('pip search %s' % name).read()
    need_update = False
    for line in text.splitlines():
        print line
        line = line.strip()
        if line.startswith('LATEST:'):
            need_update = True
    if need_update:
        print Color.red('run: pip install -U %s, update it!' % name)
