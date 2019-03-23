# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['shopify_requests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'shopify-requests',
    'version': '0.3.0',
    'description': 'Wrapper around the Shopify API using requests.',
    'long_description': "# Shopify Requests\n[![pipeline status](https://gitlab.com/perobertson/shopify-requests/badges/master/pipeline.svg)](https://gitlab.com/perobertson/shopify-requests/commits/master)\n[![coverage report](https://gitlab.com/perobertson/shopify-requests/badges/master/coverage.svg)](https://gitlab.com/perobertson/shopify-requests/commits/master)\n\nThe ShopifyRequests library is a wrapper around the python requests library.\nIts main purpose is to remove the boiler plate code needed to do basic API calls to Shopify.\n\n## Usage\n```python\nfrom shopify_requests import RestClient\n\nclient = RestClient('foo.myshopify.com', access_token='abc123')\nresponse = client.get('shop.json')\n```\nThe `RestClient` sets up the session with the correct auth and accept headers.\nMultiple requests with the client will reuse the same TCP connection.\n",
    'author': 'Paul Robertson',
    'author_email': 't.paulrobertson@gmail.com',
    'url': 'https://gitlab.com/perobertson/shopify-requests',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
