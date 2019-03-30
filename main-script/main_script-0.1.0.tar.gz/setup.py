# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['main_script']
setup_kwargs = {
    'name': 'main-script',
    'version': '0.1.0',
    'description': "A simple decorator to replace if __name__ == '__main__' with @main_script",
    'long_description': None,
    'author': 'Matt Kramer',
    'author_email': 'matthew.robert.kramer@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
