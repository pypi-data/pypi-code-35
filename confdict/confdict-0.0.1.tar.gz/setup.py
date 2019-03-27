# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['confdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'confdict',
    'version': '0.0.1',
    'description': 'A dictionary with nested access, interpolation and fallback features. It is primarily meant to be used for storing configurations of programs.',
    'long_description': "# ConfDict\n\nConfiguration dictionary that extends built-in python dict with recursive access, self references and fallback functionality. There is no extensive documentation yet, you can check out tests to figure out all features.\n\n## Example usage.\n\n```python\n>>> from confdict import ConfDict\n>>> cd = ConfDict(\n  # Configuration of ConfDict, these are default values\n  __separator = '/',\n  __self_key = '.',\n  __parent_key = '..',\n  __root_key = '...',\n  __key_key = '<key>',\n  __interpolation_regex = r'({{([^{}]*)}})',\n  __fallback_key = 'fallback',\n\n  # Remaining arguments will directly be stored in underlying dict\n  users = {\n    # fallback dict is used when a key is not found at that level\n    'fallback': {\n      # <key> is evaluated to key of the current level\n      # it is useful when used with fallback\n      'username': '{{<key>}}',\n      # you can use self references\n      'ssh_private_key': '/home/{{username}}/.ssh/id_rsa',\n    },\n  }\n)\n>>> cd\nConfDict\n{ 'users': { 'fallback': { 'ssh_private_key': '/home/{{username}}/.ssh/id_rsa',\n                           'username': '{{<key>}}'}}}\n>>> cd['users/john/username']\n'john'\n>>> cd['users/john/ssh_private_key']\n'/home/john/.ssh/id_rsa'\n>>> cd['users/john']\nConfDict\n{'ssh_private_key': '/home/john/.ssh/id_rsa', 'username': 'john'}\n>>> cd['users/jean']\nConfDict\n{'ssh_private_key': '/home/jean/.ssh/id_rsa', 'username': 'jean'}\n>>> cd['users/jean'] = { 'username': 'jeans_custom_username' }\n>>> cd['users/jean/ssh_private_key']\n'/home/jeans_custom_username/.ssh/id_rsa'\n>>> # 'jean' exists now under 'users'\n>>> # there is no partial fallback so there is no 'ssh_private_key'\n>>> cd['users/jean']\nConfDict\n{'username': 'jeans_custom_username'}\n>>> # we can realize fallback as jean to make concrete values\n>>> cd['users/fallback'].realize('jean')\n>>> cd['users/jean']\nConfDict\n{'ssh_private_key': '/home/jeans_custom_username/.ssh/id_rsa', 'username': 'jeans_custom_username'}\n>>> # interpolation still works\n>>> cd['users/jean/username'] = 'jeans_custom_username2'\n>>> cd['users/jean/ssh_private_key']\n'/home/jeans_custom_username2/.ssh/id_rsa'\n```\n\n\n## Installation\n```\n$ pip install confdict\n```\n\n## Development\n\nThere is a `Makefile` to automate commonly used development tasks.\n\n### Environment Setup\n\n```\n### create a virtualenv for development\n\n$ sudo pip install virtualenv # or your preferred way to install virtualenv\n\n$ make virtualenv # will also install dependencies\n\n$ source env/bin/activate\n\n### run pytest / coverage\n\n$ make test\n\n### before commit\n\n$ make format\n```\n",
    'author': 'Mehmet Can Ozdemir',
    'author_email': 'mefu.ozd@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
