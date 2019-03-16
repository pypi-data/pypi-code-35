import importlib
import pathlib

from .settings import SETTINGS


def get_app_components():
    for component in SETTINGS['components']:
        component = '{}.app'.format(component)
        yield importlib.import_module(component)


def project_path(*parts):
    return str(pathlib.Path(SETTINGS['root'], *parts))
