# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mudkip']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'livereload>=2.6,<3.0',
 'recommonmark>=0.5.0,<0.6.0',
 'sphinx-autodoc-typehints>=1.6,<2.0',
 'sphinx>=1.8,<2.0',
 'sphinx_rtd_theme>=0.4.3,<0.5.0',
 'tomlkit>=0.5.3,<0.6.0',
 'watchdog>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['mudkip = mudkip.cli:main']}

setup_kwargs = {
    'name': 'mudkip',
    'version': '0.1.8',
    'description': 'A friendly Sphinx wrapper',
    'long_description': '# 📘 Mudkip\n\n[![PyPI](https://img.shields.io/pypi/v/mudkip.svg)](https://pypi.org/project/mudkip/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mudkip.svg)](https://pypi.org/project/mudkip/)\n\n> A friendly Sphinx wrapper.\n\n**🚧 Work in progress 🚧**\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'url': 'https://github.com/vberlier/mudkip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
