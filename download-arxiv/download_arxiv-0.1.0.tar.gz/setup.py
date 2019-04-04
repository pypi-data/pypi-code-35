# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['download_arxiv']
install_requires = \
['arxiv>=0.3.1,<0.4.0', 'click>=7.0,<8.0', 'python-dateutil>=2.8,<3.0']

entry_points = \
{'console_scripts': ['arxiv = download_arxiv:main']}

setup_kwargs = {
    'name': 'download-arxiv',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Shun Kiyono',
    'author_email': 'kiyono@ecei.tohoku.ac.jp',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
