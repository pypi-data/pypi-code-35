# from setuptools import setup
from distutils.core import setup
project_name = 'csr_gcp_utils'
#project_ver = '1.0.0'
project_ver = '0.0.38'

setup(
    name=project_name,
    packages=["csr_cloud"],  # this must be the same as the name above
    version=project_ver,
    description='Utilities for csr1000v on GCP',
    author='Avani Vyas',
    author_email='avvyas@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-gcp/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-gcp/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'gcp', 'guestshell', 'csr1000v'],
    install_requires=[
          'oauth2client',
          'google-api-python-client',
          'ipaddress'
      ],
    classifiers=[],
    license="MIT"
)
