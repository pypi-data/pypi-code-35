# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['reg_bench',
 'reg_bench.maps',
 'reg_bench.ode',
 'reg_bench.symbolic_regression']

package_data = \
{'': ['*']}

install_requires = \
['derivative>=0.1.2,<0.2.0',
 'numpy>=1.15,<2.0',
 'pyodesys>=0.12.4,<0.13.0',
 'scikit-learn[alldeps]>=0.20.1,<0.21.0',
 'toolz>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'reg-bench',
    'version': '0.0.3',
    'description': '',
    'long_description': 'Regression benchmarks\n---\n\n[![Build Status](https://travis-ci.org/Ohjeah/regression-benchmarks.svg?branch=master)](https://travis-ci.org/Ohjeah/regression-benchmarks) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n',
    'author': 'Markus Quade',
    'author_email': 'info@markusqua.de',
    'url': 'https://github.com/Ohjeah/regression-benchmarks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
