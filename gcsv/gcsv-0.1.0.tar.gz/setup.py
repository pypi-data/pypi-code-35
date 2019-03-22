# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gcsv']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.7,<2.0',
 'google-auth-httplib2>=0.0.3,<0.0.4',
 'google-auth-oauthlib>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gcsv',
    'version': '0.1.0',
    'description': 'Easy pasting of CSV files to Google Sheets.',
    'long_description': '=====\ng-csv\n=====\nManages .csv files and uploads or pastes them to Google Sheets.\n\nUsage\n=====\n\nInstallation\n------------\n\nWith Python installed, and in a command window, enter: ``pip install gcsv``\n\nCode\n----\n\nUse the following code example as a guide, replacing the following dummy strings with relevant information.\n\n- ``my_csv_path``: the path to your CSV (e.g ``C:\\reports\\mycsv.csv``)\n- ``my_spreadsheet_id``: the ID (or "key") of a spreadsheet; can be found in the spreadsheet URL after ``/d/`` but before ``/edit``\n- ``my_worksheet_gid``: the worksheet (or "tab") name of the paste destination\n- ``start_row``: the starting row of the paste destination\n- ``start_col``: the starting column of the paste destination\n\n.. code-block:: python\n\n    import gcsv\n\n    csv = gcsv.GCSV(r\'my_csv_path\')\n\n    csv.paste_to(\'my_spreadsheet_id\',\n                 my_worksheet_gid,\n                 start_row,\n                 start_col)',
    'author': 'Liam Corbett',
    'author_email': None,
    'url': 'https://github.com/liamCorbett/g-csv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
