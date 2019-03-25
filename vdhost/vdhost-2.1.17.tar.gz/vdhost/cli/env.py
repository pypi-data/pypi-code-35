import os

"""
Any environment variables used by vdhost.
"""

# the base API url
if 'VDHOST_API_URL' in os.environ:
    BASE_API_URL = os.environ['VDHOST_API_URL']
    print('vdhost is using development URL: {}'.format(BASE_API_URL))
else:
    BASE_API_URL = 'https://api.vectordash.com'


# the Vectordash installation path
BASE_INSTALL_PATH = '/var/vectordash'

