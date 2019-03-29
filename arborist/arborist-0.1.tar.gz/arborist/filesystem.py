import os


def create_dir(dirpath):
    "Create directory tree to `dirpath`; ignore if already exists"
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    return dirpath
