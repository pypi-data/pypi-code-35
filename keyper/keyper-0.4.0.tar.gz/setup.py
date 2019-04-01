# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keyper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'keyper',
    'version': '0.4.0',
    'description': 'A utility for dealing with the macOS keychain.',
    'long_description': '# keyper \n\n[![PyPi Version](https://img.shields.io/pypi/v/keyper.svg)](https://pypi.org/project/keyper/)\n[![License](https://img.shields.io/pypi/l/keyper.svg)](https://github.com/Microsoft/keyper/blob/master/LICENSE)\n\nA Python 3 library for dealing with the macOS Keychain\n\n## Installation\n\n    pip install keyper\n\n## Examples:\n```python\nimport keyper\n\n# Get a password from the keychain\npassword = keyper.get_password(label="my_keychain_password")\n\n# Create a temporary keychain and install the certificate:\n\nwith keyper.TemporaryKeychain() as keychain:\n    certificate = keyper.Certificate("/path/to/cert", password="password")\n    keychain.install_cert(certificate)\n    # Use codesign or similar here\n```\n    \n\n\n# Contributing\n\nThis project welcomes contributions and suggestions.  Most contributions require you to agree to a\nContributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us\nthe rights to use your contribution. For details, visit https://cla.microsoft.com.\n\nWhen you submit a pull request, a CLA-bot will automatically determine whether you need to provide\na CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions\nprovided by the bot. You will only need to do this once across all repos using our CLA.\n\nThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).\nFor more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or\ncontact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.\n',
    'author': 'Dale Myers',
    'author_email': 'dalemy@microsoft.com',
    'url': 'https://github.com/Microsoft/keyper',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
