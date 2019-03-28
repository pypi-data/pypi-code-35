# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cleanser', 'cleanser.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cleanser',
    'version': '0.1.1',
    'description': 'Tools for cleaning text.',
    'long_description': '# cleanser\n[![Build Status](https://mholtzscher.visualstudio.com/cleanser/_apis/build/status/cleanser-CI?branchName=master)](https://mholtzscher.visualstudio.com/cleanser/_build/latest?definitionId=2&branchName=master)\n',
    'author': 'Michael Holtzscher',
    'author_email': 'mholtz@protonmail.com',
    'url': 'https://github.com/mholtzscher/cleanser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
