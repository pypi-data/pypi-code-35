from os.path import abspath, dirname, basename, join, exists
from os import walk


def dirreplace(
        dirpath,
        from_string,
        to_string,
        suffix=(
            'py', 'htm', 'txt', 'conf', 'css', 'h', 'template', 'js', 'html',
            'rst', 'coffee', 'yaml', 'mako', 'sh', 'wsgi', 'scss', 'less',
            'plim', 'sass', 'slm','vue','hbs',
        )
):
    from_string = from_string.strip()
    to_string = to_string.strip()
    for from_s, to_s in zip(list(filter(bool, from_string.split('\n'))),
                            list(filter(bool, to_string.split('\n')))):
        _replace(dirpath, from_s.strip(), to_s.strip(), suffix)


IGNORE = ".git .hg node_modules".split()
IGNORE = ["/%s/" % i for i in IGNORE]


def _replace(dirpath, from_string, to_string, suffix):
    from_string = from_string.strip()
    to_string = to_string.strip()

    for dirpath, dirnames, filenames in walk(dirpath):
        dirbase = basename(dirpath)
        for ignore in IGNORE:
            if ignore in dirpath:
                break
        else:
            if dirbase.startswith('.'):
                continue

            for filename in filenames:
                _suffix = filename.rsplit('.', 1)[-1]
                # if suffix not in ('css','html', 'htm', ):
                if _suffix not in suffix:
                    continue
                if filename == "replace_line.py":
                    continue
                path = join(dirpath, filename)
                if not exists(path):
                    continue
                with open(path) as f:
                    try:
                        content = f.read()
                    except:
                        print(path, "read failed")
                        continue
                t = content.replace(from_string, to_string)
                if t != content:
                    try:
                        t = t.encode('utf-8')
                    except:
                        print(path, "utf-8 failed")
                        continue
                    with open(path, 'wb') as f:
                        f.write(t)
