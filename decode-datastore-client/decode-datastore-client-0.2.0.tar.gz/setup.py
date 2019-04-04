from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='decode-datastore-client',
    version='0.2.0',
    maintainer='Sam Mulube',
    maintainer_email='sam@thingful.net',
    url='https://github.com/thingful/decode-datastore-client-py',
    description='Python client for the DECODE encrypted datastore',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'protobuf',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
