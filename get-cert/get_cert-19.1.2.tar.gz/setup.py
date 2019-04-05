# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['get_cert']
install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'get-cert',
    'version': '19.1.2',
    'description': 'Tool for downloading ssl certificates from remote servers.',
    'long_description': '# get_cert\n\nTool for downloading ssl certificates from remote servers.\n\n## Installation\n\nJust use PIP:\n\n```bash\npip install get_cert\n```\n\n## Usage\n\n```bash\n$ python -m get_cert --help\nUsage: get_cert.py [OPTIONS] URL\n\n  Retrieve and print out the ssl certificate.\n\n  Args:     URL (str): url to be picked up\n\nOptions:\n  --help  Show this message and exit.\n```\n',
    'author': 'Michal Mazurek',
    'author_email': 'michal@mazurek-inc.co.uk',
    'url': 'https://github.com/michalmazurek/get_cert',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
