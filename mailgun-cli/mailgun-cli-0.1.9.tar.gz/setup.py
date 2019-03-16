# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mailgun_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'loguru>=0.2.5,<0.3.0',
 'pandas>=0.24.1,<0.25.0',
 'tqdm>=4.31,<5.0',
 'uplink>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['mailgun = mailgun_cli.cli:main']}

setup_kwargs = {
    'name': 'mailgun-cli',
    'version': '0.1.9',
    'description': 'control mailgun account using cli and python api',
    'long_description': '# mailgun-cli\ncontrol mailgun account using cli and python api\n\n## Features\n- easily create routes for 1-on-1 forwarding mail using a csv file or Google Spreadsheet\n\n## Usages\n### CLI\nset the mailgun api key\n```bash\n# bash shell\n$ export MAILGUN_API_KEY [your private API key]\n# fish shell\n$ set -X MAILGUN_API_KEY [your private API key]\n```\nYou could permanently set it in `~/.bash_profile` or `~/.config/fish/config.fish`\n\n*list all routes*\n```bash\n$ mailgun routes\n```\n*forward using a csv*\n```bash\n$ mailgun forward "https://docs.google.com/spreadsheets/d/e/2PACX-1vQX-8YPc7Dja4jn3u0E5MzGdEOPxB9OEI2kDzO_7c-CLpGQ5g8LdPO2W9f6tETrVyBBZvWx3qNAMwPa/pub?output=csv"\n```\n\n## install\n```\n$ pip install mailgun-cli \n```\n✨🍰✨\n\n## Forward templete\nGoogle Spreadsheet, [Here is a templete](https://docs.google.com/spreadsheets/d/1JOKoNcUMIYtUiahQfP309BhpqU-5uPir1UcsAmLkKaY/edit?usp=sharing). \n   1. First publish your Google sheet to the web by going to File > Publish to the web...\n   2. Choose the tab you want, then select Comma-separated values (.csv) as the export format\n   3. Grab the URL\n\n## Learning Path\n1. https://codingdose.info/2018/08/02/develop-and-publish-with-poetry/',
    'author': 'Nutchanon Ninyawee ',
    'author_email': 'dev@nutchanon.org',
    'url': 'https://github.com/CircleOnCircles/mailgun-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
