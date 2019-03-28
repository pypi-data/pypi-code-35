# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mudkip']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'jupyter>=1.0,<2.0',
 'jupyter_nbextensions_configurator>=0.4.1,<0.5.0',
 'livereload>=2.6,<3.0',
 'nbsphinx>=0.4.2,<0.5.0',
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
    'version': '0.2.0',
    'description': 'A friendly Sphinx wrapper',
    'long_description': '# 📘 mudkip\n\n[![PyPI](https://img.shields.io/pypi/v/mudkip.svg)](https://pypi.org/project/mudkip/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mudkip.svg)](https://pypi.org/project/mudkip/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A friendly [Sphinx](sphinx-doc.org) wrapper.\n\n**🚧 Work in progress 🚧**\n\nMudkip is a small wrapper around [Sphinx](sphinx-doc.org) that bundles essential tools and extensions, providing everything needed for most day-to-day documentation.\n\n```bash\n$ mudkip --help\nUsage: mudkip [OPTIONS] COMMAND [ARGS]...\n\n  A friendly Sphinx wrapper.\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  build    Build documentation.\n  clean    Remove output directory.\n  develop  Start development server.\n  init     Initialize documentation.\n  test     Test documentation.\n```\n\n## Features\n\nMudkip intends to provide an out-of-the-box solution for small to medium projects. The command-line utility lets you build and check your documentation, launch a development server with live reloading, run doctests and more!\n\nMudkip enables the following Sphinx extensions:\n\n- [`sphinx.ext.autodoc`](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) for generating documentation from docstrings\n- [`sphinx.ext.napoleon`](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) for Google-style and NumPy-style docstrings support\n- [`sphinx_autodoc_typehints`](https://github.com/agronholm/sphinx-autodoc-typehints) for pulling type information from Python 3 annotations\n- [`sphinx.ext.doctest`](https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html) for doctest support\n- [`recommonmark`](https://recommonmark.readthedocs.io/en/latest/) for markdown support\n- [`nbsphinx`](https://nbsphinx.readthedocs.io) for Jupyter notebook support\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install mudkip\n```\n\n## Usage\n\n> **TODO**\n\n## Contributing\n\nContributions are welcome. This project uses [poetry](https://poetry.eustace.io/).\n\n```bash\n$ poetry install\n```\n\nThe code follows the [black](https://github.com/ambv/black) code style.\n\n```bash\n$ poetry run black mudkip\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/mudkip/blob/master/LICENSE)\n',
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
