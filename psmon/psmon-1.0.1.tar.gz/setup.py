# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['psmon', 'psmon.limiters']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.2.5,<0.3.0', 'psutil>=5.5,<6.0']

setup_kwargs = {
    'name': 'psmon',
    'version': '1.0.1',
    'description': 'Process monitoring',
    'long_description': '# psmon\n\n[![Travis (.com)](https://img.shields.io/travis/com/rkkautsar/psmon.svg)](https://travis-ci.com/rkkautsar/psmon)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psmon.svg)](https://pypi.org/project/psmon)\n[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=rkkautsar/psmon)](https://dependabot.com)\n\nMonitors and limits process resource\n',
    'author': 'Rakha Kanz Kautsar',
    'author_email': 'rkkautsar@gmail.com',
    'url': 'https://github.com/rkkautsar/psmon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
