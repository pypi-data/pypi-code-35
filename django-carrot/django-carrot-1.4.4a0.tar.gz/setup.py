# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['carrot',
 'carrot.management',
 'carrot.management.commands',
 'carrot.migrations']

package_data = \
{'': ['*'], 'carrot': ['static/carrot/*', 'templates/carrot/*']}

install_requires = \
['django>=2.1,<3.0',
 'djangorestframework>=3.9,<4.0',
 'json2html>=1.2,<2.0',
 'pika>=0.13.1,<0.14.0',
 'psutil>=5.6,<6.0',
 'sphinx_bootstrap_theme>=0.6.5,<0.7.0']

setup_kwargs = {
    'name': 'django-carrot',
    'version': '1.4.4a0',
    'description': 'A RabbitMQ asynchronous task queue for Django.',
    'long_description': ".. image:: https://coveralls.io/repos/github/chris104957/django-carrot/badge.svg?branch=master\n    :target: https://coveralls.io/github/chris104957/django-carrot?branch=master\n\n.. image:: https://readthedocs.org/projects/django-carrot/badge/?version=latest\n    :target: http://django-carrot.readthedocs.io/en/latest/?badge=\n\n.. image:: https://travis-ci.org/chris104957/django-carrot.svg?branch=master\n    :target: https://travis-ci.org/chris104957/django-carrot.svg?branch=master\n\n.. image:: https://coveralls.io/repos/github/chris104957/django-carrot/badge.svg?branch=master\n    :target: https://coveralls.io/github/chris104957/django-carrot?branch=master)\n\n.. image:: https://badge.fury.io/py/django-carrot.svg\n    :target: https://badge.fury.io/py/django-carrot\n\n.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg\n    :target: https://opensource.org/licenses/Apache-2.0\n\n.. image:: /docs/source/images/carrot-logo-big.png\n    :align: center\n\n**django-carrot** is a lightweight task queue backend for Django projects that uses the RabbitMQ message broker, with\nan emphasis on quick and easy configuration and task tracking\n\nInstallation\n------------\n\nInstall django-carrot:\n\n.. code-block:: bash\n\n    pip install django-carrot\n\nInstall and run RabbitMQ\n\n.. code-block:: bash\n\n    brew install rabbitmq\n    brew services start rabbitmq\n\nConfiguration\n-------------\n\n1. Add carrot to your Django project's settings module:\n\n.. code-block:: python\n\n    INSTALLED_APPS = [\n        ...\n        'carrot',\n        ...\n    ]\n\n\n2. Apply the carrot migrations to your project's database:\n\n.. code-block:: python\n\n    python manage.py migrate carrot\n\n\nUsage\n-----\n\nTo start the service:\n\n.. code-block:: bash\n\n    python manage.py carrot_daemon start\n\n\nTo run tasks asynchronously:\n\n.. code-block:: python\n\n    from carrot.utilities import publish_message\n\n    def my_task(**kwargs):\n        return 'hello world'\n\n    publish_message(my_task, hello=True)\n\n\n\nTo schedule tasks to run at a given interval\n\n.. code-block:: python\n\n    from carrot.utilities import create_scheduled_task\n\n    create_scheduled_task(my_task, {'seconds': 5}, hello=True)\n\n\n.. note::\n    The above commands must be made from within the Django environment\n\nDocker\n------\n\nA sample docker config is available `here <https://github.com/chris104957/django-carrot-docker>`_\n\nFull documentation\n------------------\n\nThe full documentation is available `here <https://django-carrot.readthedocs.io/>`_\n\nSupport\n-------\n\nIf you are having any issues, please `log an issue <https://github.com/chris104957/django-carrot/issues/new>`_\n\nContributing\n------------\n\nDjango-carrot uses `Packagr <https://www.packagr.app/>`_ to share development builds. If you'd like access to it,\nplease send me your email address at christopherdavies553@gmail.com so I can give you access\n\nLicense\n-------\n\nThe project is licensed under the Apache license.\n\nIcons made by Trinh Ho from `www.flaticon.com <www.flaticon.com>`_ is licensed by CC 3.0 BY\n",
    'author': 'Christoper Davies',
    'author_email': 'christopherdavies553@gmail.com',
    'url': 'https://django-carrot.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
