# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['naipyext']

package_data = \
{'': ['*']}

install_requires = \
['better_exceptions', 'ipython>=7.2,<8.0']

extras_require = \
{'all': ['requests_html>=0.9.0,<0.10.0',
         'requests>=2.21,<3.0',
         'numpy>=1.15,<2.0',
         'jupyter>=1.0,<2.0',
         'sympy>=1.3,<2.0',
         'pandas>=0.23.4,<0.24.0',
         'pendulum>=2.0,<3.0',
         'tqdm>=4.28,<5.0',
         'bs4>=0.0.1,<0.0.2'],
 'math': ['numpy>=1.15,<2.0',
          'jupyter>=1.0,<2.0',
          'sympy>=1.3,<2.0',
          'pandas>=0.23.4,<0.24.0'],
 'others': ['requests_html>=0.9.0,<0.10.0',
            'requests>=2.21,<3.0',
            'pendulum>=2.0,<3.0',
            'tqdm>=4.28,<5.0',
            'bs4>=0.0.1,<0.0.2']}

setup_kwargs = {
    'name': 'naipyext',
    'version': '0.2.0',
    'description': 'Nasy IPython Extensions.',
    'long_description': None,
    'author': 'Nasy',
    'author_email': 'nasyxx+python@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
