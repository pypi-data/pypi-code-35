import setuptools
from distutils.core import setup

project_name = 'csr_aws_utils'
project_ver = '1.0.0'

setup(
    name=project_name,
    packages=["csr_cloud"],  # this must be the same as the name above
    install_requires=['boto3', 'requests'],
    version=project_ver,
    description='Utilities for csr1000v on AWS',
    author='Christopher Reder',
    author_email='creder@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-aws/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-aws/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'aws', 'guestshell', 'csr1000v'],
    classifiers=[],
    license="MIT"
)
