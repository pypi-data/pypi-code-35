# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dnsdb']

package_data = \
{'': ['*']}

install_requires = \
['diskcache>=3.1,<4.0', 'python-dateutil>=2.8,<3.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'dnsdb',
    'version': '0.2.4',
    'description': "Python client for Farsight Security's DNSDB API",
    'long_description': '# dnsdb\n\nPython client for Farsight Security\'s [DNSDB API](https://api.dnsdb.info/).\n\n## Features\n\n * supports all capabilities of [DNSDB API](https://api.dnsdb.info/)\n * sorting of results by last_seen\n * convert epoch to ISO 8601\n * normalize results with regard sensor or zone observation\n * supports the caching of DNSDB API results\n * returns an object with the following attributes:\n    * records\n    * status code\n    * error\n    * quota\n    * cache\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install [dnsdb](https://pypi.org/project/dnsdb/).\n\n```bash\npip install dnsdb\n```\n\n## Usage\n\n### Setup\n```text\n>>> from dnsdb import Dnsdb\n\n>>> api_key="12345"\n>>> dnsdb = Dnsdb(api_key)\n```\n\n### Example 1\n```text\n>>> result = dnsdb.search(name="www.example.com")\n\n>>> pprint(result.status_code)\n200\n\n>>> pprint(result.error)\nNone\n\n>>> pprint(result.records[0])\n{\'bailiwick\': \'example.com.\',\n \'count\': 4213726,\n \'rdata\': [\'93.184.216.34\'],\n \'rrname\': \'www.example.com.\',\n \'rrtype\': \'A\',\n \'source\': \'sensor\',\n \'time_first\': \'2014-12-10T00:19:18Z\',\n \'time_last\': \'2019-03-05T14:37:31Z\'}\n \n>>> pprint(result.quota)\n{\'expires\': None,\n \'limit\': \'1000000\',\n \'remaining\': \'999970\',\n \'reset\': \'1551830400\',\n \'results_max\': None}\n```\n\n### Example 2\n```text\n>>> result = dnsdb.search(name="hello.example.com")\n\n>>> pprint(result.status_code)\n404\n\n>>> pprint(result.error)\n{\'code\': 404, \'message\': \'Error: no results found for query.\'}\n\n>>> pprint(result.records)\nNone\n\n>>> pprint(result.quota)\n{\'expires\': None,\n \'limit\': \'1000000\',\n \'remaining\': \'999969\',\n \'reset\': \'1551830400\',\n \'results_max\': None}\n```\n\n## More Usage\n```text\nfrom dnsdb import Dnsdb\n\napi_key="12345"\ndnsdb = Dnsdb(api_key)\ndnsdb = Dnsdb(api_key, cache=True)\ndnsdb = Dnsdb(api_key, cache=True, cache_timeout=900)\ndnsdb = Dnsdb(api_key, cache=True, cache_location="/tmp/dnsdb-cache")\n\nresult = dnsdb.search(name="fsi.io")\nresult = dnsdb.search(name="mail.fsi.io", inverse=True)\nresult = dnsdb.search(ip="104.244.14.108")\nresult = dnsdb.search(ip="104.244.14.0/24")\nresult = dnsdb.search(ip="2620:11c:f008::108")\nresult = dnsdb.search(hexadecimal="36757a35")\nresult = dnsdb.search(name="fsi.io", type="A")\nresult = dnsdb.search(name="farsightsecurity.com", bailiwick="com.")\nresult = dnsdb.search(name="fsi.io", wildcard_left=True)\nresult = dnsdb.search(name="fsi", wildcard_right=True)\nresult = dnsdb.search(name="fsi.io", sort=False)\nresult = dnsdb.search(name="fsi.io", remote_limit=150000, return_limit=1000)\nresult = dnsdb.search(name="fsi.io", time_last_after="2019-01-01")\nresult = dnsdb.search(name="fsi.io", time_last_after="2019-01-01T00:00:00Z")\nresult = dnsdb.search(name="fsi.io", epoch=True, time_last_after=1546300800)\nresult = dnsdb.search(name="fsi.io", epoch=True)\nresult = dnsdb.quota()\n```\n\n## Contributing\nPull requests are welcome; for major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to create and update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Gabriel Iovino',
    'author_email': 'giovino@gmail.com',
    'url': 'https://github.com/giovino/fsi-dnsdb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
