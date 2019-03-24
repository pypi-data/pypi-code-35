# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioapi', 'aioapi.inspect']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5.4', 'pydantic>=0.20.1']

setup_kwargs = {
    'name': 'aioapi',
    'version': '0.2.0a0',
    'description': 'Yet another way to build APIs using AIOHTTP framework',
    'long_description': "# aioapi\n\nYet another way to build APIs using [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework.\n\n## Installation\n\n```sh\n$ pip install aioapi\n```\n\n## Usage\n\nExamples of usage can be found at `examples` directory.\n\nTo run example use command below:\n\n```sh\n$ make example\n```\n\n## Contributing\n\nTo work on the `aioapi` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/aioapi.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify what you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## Milestones\n\nIf you're interesting in project's future you can find milestones and plans at [projects](https://github.com/Gr1N/aioapi/projects) page.\n\n## License\n\n`aioapi` is licensed under the MIT license. See the license file for details.\n",
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'url': 'https://github.com/Gr1N/aioapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
