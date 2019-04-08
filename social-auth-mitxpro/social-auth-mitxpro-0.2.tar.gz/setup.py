# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['social_auth_mitxpro']

package_data = \
{'': ['*']}

install_requires = \
['social-auth-core>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'social-auth-mitxpro',
    'version': '0.2',
    'description': 'python-social-auth backend for mitxpro',
    'long_description': "\nsocial-auth-mitxpro\n---\n\n\n#### Prerequisites\n\n- [`pyenv`](https://github.com/pyenv/pyenv#installation) for managing python versions\n  - Install `python3.6` and `python2.7`\n- `pip install tox tox-pyenv` for running tests and discovering python versions from `pyenv`\n- [`poetry`](https://poetry.eustace.io/docs/#installation) for building, testing, and releasing\n\nIf this is your first time using `poetry`, you'll need to configure your pypi credentials via:\n- Configure pypi repository:\n  - `poetry config http-basic.pypi USERNAME PASSWORD`\n- Configure testpypi repository:\n  - `poetry config repositories.testpypi https://test.pypi.org/legacy`\n  - `poetry config http-basic.testpypi USERNAME PASSWORD`\n\n**NOTE:** when running `poetry` commands, particularly `pylint` and `black`, you must `python3.6`\n\n#### Testing\n\nYou can just run `tox` locally to test, lint, and check formatting in the supported python versions. This works by having `tox` manage the virtualenvs, which `poetry` then detects and uses. Note that some of the tools (e.g. `pylint`, `black`) only support running in `python3.6` and this is reflected in `tox.ini`.\n\nRun individual commands can be run interactively in a `poetry shell` session or directly via `poetry run CMD`:\n\n- `pytest` - run python tests\n- `pylint` - lint python code\n- `black .` - format python code\n\n#### Building\n\n- `poetry build` - builds a pip-installable package into `dist/`\n\n#### Releasing\n\n- `poetry version VERSION` - bump the project version (see `poetry version --help` for details)\n- `poetry publish -r testpypi` - publish to testpypi\n- `poetry publish` - publish to pypi\n",
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'url': 'https://pypi.org/project/social-auth-mitxpro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
