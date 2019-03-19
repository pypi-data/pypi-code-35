# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['toodledo']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=2.16,<3.0', 'requests-oauthlib>=1.0,<2.0', 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'toodledo',
    'version': '1.0.0',
    'description': 'Python wrapper for the Toodledo v3 API which is documented at http://api.toodledo.com/3/',
    'long_description': 'Overview\n========\nPython wrapper for the Toodledo v3 API which is documented at http://api.toodledo.com/3/\n\n.. image:: https://travis-ci.org/rkhwaja/toodledo-python.svg?branch=master\n   :target: https://travis-ci.org/rkhwaja/toodledo-python\n\nUsage\n=====\n\n.. code-block:: python\n\n  toodledo = Toodledo(\n    clientId="YourClientId",\n    clientSecret="YourClientSecret",\n    tokenStorage=TokenStorageFile(YourConfigFile),\n    scope="basic tasks notes folders write")\n\n  account = toodledo.GetAccount()\n\n  allTasks = toodledo.GetTasks(params={})\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'url': 'https://github.com/rkhwaja/toodledo-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
