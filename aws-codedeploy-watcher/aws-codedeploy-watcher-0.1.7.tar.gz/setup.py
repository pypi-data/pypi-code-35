# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aws_codedeploy_watcher']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'botocore>=1.12,<2.0', 'pendulum>=2.0,<3.0']

entry_points = \
{'console_scripts': ['aws-codedeploy-watcher = aws_codedeploy_watcher:main']}

setup_kwargs = {
    'name': 'aws-codedeploy-watcher',
    'version': '0.1.7',
    'description': 'Observe AWS Codedeploy deployments live',
    'long_description': None,
    'author': 'Daniel Miranda',
    'author_email': 'danielkza2@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
