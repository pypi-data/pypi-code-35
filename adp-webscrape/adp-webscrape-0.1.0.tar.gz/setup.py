# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['adpwebscrape']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141,<4.0']

setup_kwargs = {
    'name': 'adp-webscrape',
    'version': '0.1.0',
    'description': 'Log into and download reports from ADP Resource and ezLaborManager.',
    'long_description': '====================\nADP website scraping\n====================\nA Selenium-based python script for logging into ADP Resource and downloading reports.\n\n\nUsage\n=====\n\nInstallation\n------------\nWith Python 3.6 or greater installed, in a command prompt: enter ``pip install adp-webscrape``. You\'ll also need a recent edition of Firefox and its respective GeckoDriver_. The GeckoDriver must be added to PATH, or to the root folder of the project.\n\n.. _GeckoDriver: https://github.com/mozilla/geckodriver/releases\n\nCode\n----\nUse the following code, replacing my_username, my_password, my_download_path, and my_isi_client_id with relevant information.\n\n- ``my_username``: Your ADP Resource username\n- ``my_password``: Your ADP Resource password\n- ``my_download_path``: (optional) The path that Selenium\'s browser will download reports to (e.g ``C:\\adp-reports``). Ommiting defaults to the user\'s download folder.\n- ``my_isi_client_id``: This can be found at the end of the url for any ezLaborManager page. Most likely, it\'s going to be your company name (probably spaced out by hyphens if the name is multiple words).\n- ``my_report_index``: On the ezLaborManager "My Reports" page, this will be the index of the report you want to download (with the first report starting at index 0) https://i.imgur.com/Tg7kPQV.png\n- ``my_file_prefix``: (optional) If you\'d like to prefix the name of your files with some word so as to not mix report names, you may do so here.\n\n.. code-block:: python\n\n    import atexit\n    from adpwebscrape import ADPResource\n\n\n    resource = ADPResource(\'my_username\', \'my_password\',\n                               isi_client_id=\'my_isi_client_id\',\n                               download_path=r\'my_download_path\') \n                               \n    resource.download_my_report(my_report_index, prefix=\'my_file_prefix\') #returns Filename\n\n    atexit.register(resource.quit)\n\nOther\n=====\n\nWhy no official API?\n--------------------\nThere isn\'t one. ADP Marketplace has an API, though it is very separate from the reports I\'ve attempted to generate here.\n\nWhy Selenium and not regular schmegular requests?\n-------------------------------------------------\nRequests to ADP Resource require hidden fields whose contents seem like a pain to generate programatically. Selenium was chosen because it handles all of that at the cost of a little performance. Please let me know if you find a better way to do this.\n',
    'author': 'Liam Corbett',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
