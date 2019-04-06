# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiodogstatsd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiodogstatsd',
    'version': '0.2.0',
    'description': 'An asyncio-based client for sending metrics to StatsD with support of DogStatsD extension',
    'long_description': '# aiodogstatsd\n\n![GitHub commit merge status](https://img.shields.io/github/commit-status/Gr1N/aiodogstatsd/master/HEAD.svg?label=build%20status) [![codecov](https://codecov.io/gh/Gr1N/aiodogstatsd/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aiodogstatsd) ![PyPI](https://img.shields.io/pypi/v/aiodogstatsd.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aiodogstatsd.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aiodogstatsd.svg)\n\nAn asyncio-based client for sending metrics to StatsD with support of [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/) extension.\n\nLibrary fully tested with [statsd_exporter](https://github.com/prometheus/statsd_exporter) and supports `gauge`, `counter`, `histogram`, `distribution` and `timing` types.\n\n## Installation\n\n```sh\n$ pip install aiodogstatsd\n```\n\n## Usage\n\nYou can simply initialize client to send any metric you want:\n\n```python\nimport asyncio\n\nimport aiodogstatsd\n\n\nasync def main():\n    client = aiodogstatsd.Client()\n    await client.connect()\n\n    client.increment("users.online")\n\n    await client.close()\n\n\nasyncio.run(main())\n```\n\n...or you can also use client as a context manager:\n\n```python\nimport asyncio\n\nimport aiodogstatsd\n\n\nasync def main():\n    async with aiodogstatsd.Client() as client:\n      client.increment("users.online")\n\n\nasyncio.run(main())\n```\n\nLook at `examples/` to find more examples of library usage.\n\n## Contributing\n\nTo work on the `aiodogstatsd` codebase, you\'ll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/aiodogstatsd.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## License\n\n`aiodogstatsd` is licensed under the MIT license. See the license file for details.\n',
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'url': 'https://github.com/Gr1N/aiodogstatsd',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
