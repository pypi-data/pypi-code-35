from importlib import import_module
import sys
import os

def import_obj(path):
    # Ensure the current directory is on the path
    current_dir = os.path.abspath('.')
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    # Split the object name and the module path
    module_path, handler_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, handler_name)
    for attr in module_path.split('.')[1:]:
        module = getattr(module, attr)
    obj = getattr(module, handler_name)
    if obj is None:
        raise ValueError('Unable to import object: {}'.format(path))
    return obj
