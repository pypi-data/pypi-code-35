# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['reprobench',
 'reprobench.executors',
 'reprobench.runners',
 'reprobench.runners.slurm']

package_data = \
{'': ['*'], 'reprobench': ['console/*', 'core/*', 'tools/*']}

install_requires = \
['apsw>=3.9,<4.0',
 'click>=7.0,<8.0',
 'loguru>=0.2.5,<0.3.0',
 'peewee>=3.9,<4.0',
 'psmon>=1.0.0,<2.0.0',
 'pynisher>=0.5.0,<0.6.0',
 'strictyaml>=1.0,<2.0',
 'tqdm>=4.31,<5.0']

entry_points = \
{'console_scripts': ['reprobench = reprobench.console.main:cli']}

setup_kwargs = {
    'name': 'reprobench',
    'version': '0.3.0',
    'description': 'Reproducible Benchmark for Everyone',
    'long_description': '# reprobench\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/reprobench.svg)](https://pypi.org/project/reprobench)\n[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=rkkautsar/reprobench)](https://dependabot.com)\n',
    'author': 'Rakha Kanz Kautsar',
    'author_email': 'rkkautsar@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
