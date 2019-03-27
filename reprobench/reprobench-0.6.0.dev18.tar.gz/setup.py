# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['reprobench',
 'reprobench.executors',
 'reprobench.runners',
 'reprobench.runners.local',
 'reprobench.runners.slurm',
 'reprobench.task_sources',
 'reprobench.task_sources.doi']

package_data = \
{'': ['*'], 'reprobench': ['console/*', 'core/*', 'tools/*']}

install_requires = \
['apsw>=3.9,<4.0',
 'click>=7.0,<8.0',
 'gevent>=1.4,<2.0',
 'loguru>=0.2.5,<0.3.0',
 'msgpack-python>=0.5.6,<0.6.0',
 'pathspec>=0.5.9,<0.6.0',
 'peewee>=3.9,<4.0',
 'psmon>=1.1.0,<2.0.0',
 'psutil>=5.6,<6.0',
 'py-cpuinfo>=4,<6',
 'pynisher>=0.5.0,<0.6.0',
 'pyzmq>=18.0,<19.0',
 'requests>=2.21,<3.0',
 'strictyaml>=1.0,<2.0',
 'tqdm>=4.31,<5.0']

entry_points = \
{'console_scripts': ['reprobench = reprobench.console.main:cli']}

setup_kwargs = {
    'name': 'reprobench',
    'version': '0.6.0.dev18',
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
