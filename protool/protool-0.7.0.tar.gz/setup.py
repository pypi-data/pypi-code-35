# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['protool']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['protool = protool:command_line.run']}

setup_kwargs = {
    'name': 'protool',
    'version': '0.7.0',
    'description': 'A tool for dealing with provisioning profiles',
    'long_description': '# protool \n\n[![PyPi Version](https://img.shields.io/pypi/v/protool.svg)](https://pypi.org/project/protool/)\n[![License](https://img.shields.io/pypi/l/protool.svg)](https://github.com/Microsoft/protool/blob/master/LICENSE)\n\nA tool for dealing with provisioning profiles.\n\nWhat can it do? \n\n* Read profiles as XML or as a dictionary\n* Read the values from the profile\n* Diff two profiles to see what has changed\n\n### Installation\n\n    pip install protool\n\n### Examples:\n\n    import protool\n    profile = protool.ProvisioningProfile("/path/to/profile")\n\n    # Get the diff of two profiles\n    diff = protool.diff("/path/to/first", "/path/to/second", tool_override="diff")\n\n    # Get the UUID of a profile\n    print profile.uuid\n\n    # Get the full XML of the profile\n    print profile.xml\n\n    # Get the parsed contents of the profile as a dictionary\n    print profile.contents()\n\n\nAlternatively, from the command line:\n\n    # Get the diff\n    protool diff --profiles /path/to/profile1 /path/to/profile2 --tool diff\n\n    # Get the UUID of a profile\n    protool read --profile /path/to/profile --key UUID\n\n    # Get the raw XML (identical to using `security cms -D -i /path/to/profile`)\n    protool decode --profile /path/to/profile\n\n\n# Contributing\n\nThis project welcomes contributions and suggestions.  Most contributions require you to agree to a\nContributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us\nthe rights to use your contribution. For details, visit https://cla.microsoft.com.\n\nWhen you submit a pull request, a CLA-bot will automatically determine whether you need to provide\na CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions\nprovided by the bot. You will only need to do this once across all repos using our CLA.\n\nThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).\nFor more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or\ncontact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.\n',
    'author': 'Dale Myers',
    'author_email': 'dalemy@microsoft.com',
    'url': 'https://github.com/Microsoft/protool',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
