# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dataland',
 'dataland.gcloud',
 'dataland.gcloud.bigquery',
 'dataland.gcloud.dataproc',
 'dataland.gcloud.storage',
 'dataland.nlp']

package_data = \
{'': ['*']}

install_requires = \
['cattrs>=0.9.0,<0.10.0',
 'google-api-core>=1.8,<1.9',
 'google-api-python-client>=1.7,<1.8',
 'google-auth-httplib2>=0.0,<0.1',
 'google-auth>=1.5,<1.6',
 'google-cloud-bigquery>=1.5,<1.6',
 'google-cloud-core>=0.28,<0.29',
 'google-cloud-dataproc>=0.3,<0.4',
 'google-cloud-storage>=1.11,<1.12',
 'google-resumable-media>=0.3,<0.4',
 'googleapis-common-protos>=1.5,<1.6',
 'oauth2client>=3.0,<3.1',
 'pyspark>=2.3,<2.4',
 'python-box>=3.2,<4.0',
 'python-dateutil>=2.8,<3.0',
 'regex>=2019.2,<2020.0',
 'zhon>=1.1,<2.0']

setup_kwargs = {
    'name': 'dataland',
    'version': '0.1.7',
    'description': 'Miscellaneous utilities and tools for daily data research/developments',
    'long_description': None,
    'author': 'Ryan',
    'author_email': 'ryanchao2012@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
