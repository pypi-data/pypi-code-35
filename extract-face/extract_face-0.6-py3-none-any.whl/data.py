import os


def _name2path(name):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(data_path, name)


haarcascade_frontalface_default = _name2path('haarcascade_frontalface_default.xml')