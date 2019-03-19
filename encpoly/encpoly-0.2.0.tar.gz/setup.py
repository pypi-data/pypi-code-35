# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['encpoly']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'encpoly',
    'version': '0.2.0',
    'description': "Library for encoding/decoding geographic coordinates using Google's Encoded Polyline Algorithm",
    'long_description': 'The `encpoly` package is a Python 3 library for fast, Pythonic manipulation of [encoded polylines][].\n\n[![Build status][tci]][tcl]\n[![Code coverage report][cci]][ccl]\n[![Package on PyPI][ppi]][ppl]\n\n```python\n>>> from encpoly import encode, decode\n>>> coords = ((38.5, -120.2), (40.7, -120.95), (43.252, -126.453))\n>>> encode(coords)\n\'_p~iF~ps|U_ulLnnqC_mqNvxq`@\'\n>>> tuple(decode("_p~iF~ps|U_ulLnnqC_mqNvxq`@"))\n([38.5, -120.2], [40.7, -120.95], [43.252, -126.453])\n```\n\nYou can use Pip to install the [latest release][] from PyPi:\n\n    pip install encpoly\n\n  [encoded polylines]: https://developers.google.com/maps/documentation/utilities/polylinealgorithm\n  [tci]: https://travis-ci.org/JaGallup/encpoly.svg?branch=master\n  [tcl]: https://travis-ci.org/JaGallup/encpoly\n  [cci]: https://img.shields.io/codecov/c/github/JaGallup/encpoly.svg\n  [ccl]: https://codecov.io/gh/JaGallup/encpoly\n  [ppi]: https://img.shields.io/pypi/v/encpoly.svg\n  [ppl]: https://pypi.org/project/encpoly/\n  [latest release]: https://github.com/JaGallup/encpoly/releases\n',
    'author': 'Matt Riggott',
    'author_email': 'matt.riggott@gmail.com',
    'url': 'https://github.com/JaGallup/encpoly',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
