# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pytorch_revgrad']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.0,<2.0']

setup_kwargs = {
    'name': 'pytorch-revgrad',
    'version': '0.0.1',
    'description': 'Gradient reversal layer for pytorch.',
    'long_description': '# `pytorch-revgrad`\n\nThis package implements a gradient reversal layer for pytorch modules.\n\n## Example usage\n\n```python\nimport torch\n\nfrom pytorch_revgrad import RevGrad\n\nmodel = torch.nn.Sequential(\n    torch.nn.Linear(10, 5),\n    torch.nn.Linear(5, 2),\n    RevGrad()\n)\n```\n',
    'author': 'Jan Freyberg',
    'author_email': 'jan.freyberg@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
