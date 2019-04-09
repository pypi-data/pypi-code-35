# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['py_wave_runup']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0']

setup_kwargs = {
    'name': 'py-wave-runup',
    'version': '0.1.1',
    'description': 'Empirical wave runup models implemented in Python',
    'long_description': '=================\nPython Wave Runup\n=================\n\n\n.. image:: https://img.shields.io/pypi/v/py-wave-runup.svg\n        :target: https://pypi.python.org/pypi/py-wave-runup\n\n.. image:: https://img.shields.io/travis/com/chrisleaman/py-wave-runup.svg\n        :target: https://travis-ci.com/chrisleaman/py-wave-runup\n\n.. image:: https://readthedocs.org/projects/py-wave-runup/badge/?version=latest\n    :target: https://py-wave-runup.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/chrisleaman/py-wave-runup/shield.svg\n     :target: https://pyup.io/repos/github/chrisleaman/py-wave-runup/\n     :alt: Updates\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nEmpirical wave runup models implemented in Python\n\n\n* Free software: GNU General Public License v3\n* Documentation: https://py-wave-runup.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Chris Leaman',
    'author_email': None,
    'url': 'https://github.com/chrisleaman/py-wave-runup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
