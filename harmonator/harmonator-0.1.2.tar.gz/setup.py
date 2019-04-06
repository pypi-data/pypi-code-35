# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['harmonator']

package_data = \
{'': ['*'], 'harmonator': ['exceptions/*']}

install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'harmonator',
    'version': '0.1.2',
    'description': 'Harmontown Downloader',
    'long_description': '|black| |codacy_grade| |codacy_coverage| |pypi_python_version| |pypi_status|\n\nHarmonator\n==========\n\nThe Harmontown downloader\n\nRunning this application will get you up to date with the latest episodes of Harmontown. Filename\nformatting is automatic and complies to the following format::\n\n    harmontown - S01E01 - Episode title.mp3\n\nInstallation\n------------\n\nHarmonator can be installed with pip::\n\n    pip install harmonator\n\nUsage\n-----\n\nHarmonator is used from the command line and cen be used to download either a single episode,\nepisodes after a date, or all missing episodes.\n\nDownload a single episode by episode number::\n\n    harmonate.py --episode=100\n\nAuthors:\n--------\n\nCreated by Chris Read\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.png\n    :target: https://github.com/ambv/black\n    :alt: Black\n\n.. |codacy_grade| image:: https://api.codacy.com/project/badge/Grade/84ac7eba61ef49448fc7f8fa647927b0\n    :target: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Centurix/harmonator&amp;utm_campaign=Badge_Grade\n\n.. |codacy_coverage| image:: https://api.codacy.com/project/badge/Coverage/84ac7eba61ef49448fc7f8fa647927b0\n    :target: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Centurix/harmonator&amp;utm_campaign=Badge_Coverage\n\n.. |pypi_python_version| image:: https://img.shields.io/pypi/pyversions/harmonator.png\n    :alt: PyPI - Python Version\n\n.. |pypi_status| image:: https://img.shields.io/pypi/status/harmonator.png\n    :alt: PyPI - Status\n',
    'author': 'Chris Read',
    'author_email': 'centurix@gmail.com',
    'url': 'https://github.com/Centurix/harmonator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
