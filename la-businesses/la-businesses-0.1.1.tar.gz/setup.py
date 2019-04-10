# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['la_businesses']

package_data = \
{'': ['*'],
 'la_businesses': ['.git/objects/08/*',
                   '.git/objects/4b/*',
                   '.git/objects/58/*',
                   '.git/objects/b5/*',
                   '.git/objects/d8/*']}

install_requires = \
['pandas>=0.24.2,<0.25.0',
 'pytz>=2018.9,<2019.0',
 'requests>=2.21,<3.0',
 'simplekml>=1.3,<2.0']

entry_points = \
{'console_scripts': ['la-businesses = la_businesses:main']}

setup_kwargs = {
    'name': 'la-businesses',
    'version': '0.1.1',
    'description': 'Save the latest database of businesses in Los Angeles as CSV and KML.',
    'long_description': "# la-businesses\n\n## Description\nThis script downloads and processes the listing of all active businesses \ncurrently registered with the City of Los Angeles Office of Finance. \nAn 'active' business is defined as a registered business whose owner has not \nnotified the Office of Finance of a cease of business operations. \nUpdate Interval: Monthly.\n\nData source: https://data.lacity.org/A-Prosperous-City/Listing-of-Active-Businesses/6rrh-rzua\n\nThis script fetches the data and saves it locally as a CSV file. It also selects\na subset of businesses with operation starting date within the last NDAYS days\n(default 30) and saves this as a separate CSV file. Finally, it creates and \nsaves a KML file from the subset, useful for importing into Google Maps or\nsimilar software to visualize the distribution of recent businesses opened in\nthe Los Angeles area. \n\n\n## Installation\nInstall with pip. The package installs as a command-line script. \n```\npip install la-businesses\n```\n\n## Usage\nRun from the command line (it installs as as script). All downloaded and \ngenerated files will be stored in a directory `files` inside the current \nworking directory.\n```\nusage: la-businesses [-h] [-u] [-d NDAYS]\n\noptional arguments:\n  -h, --help              show this help message and exit\n  -u, --update            update data (default: False)\n  -d NDAYS, --days NDAYS  started since NDAYS days ago (default: 30)\n```\n  \n## Known issues\n#### Locations with missing coordinates are omitted from KML file\nThe script relies on coordinate data already provided in the downloaded dataset. \nSome businesses contain addresses but no coordinates; in these cases, the \nbusiness is ignored when creating the KML (but is included in any saved CSV \nfile). Future implementations should include a function to look up location\ncoordinates from a given address (e.g., using the Open Street Maps API). \n\n#### Locations with no DBA name simply show NaN in the KML file\nThe script could use better handling of business name / DBA combinations to \nomit NaN from KML when it does not have a business name. \n\n#### No phone numbers\nThe data does not include any phone or email contact information; merging this\ndataset with one that includes contact information would be more useful for \nmarket research. \n",
    'author': 'Manuel Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
