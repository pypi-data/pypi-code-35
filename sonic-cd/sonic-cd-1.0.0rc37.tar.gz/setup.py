import os
from setuptools import setup


def get_version():
    version = '0.0.0-rc'
    tag = os.environ.get('TRAVIS_TAG')
    build_number = os.environ.get('TRAVIS_BUILD_NUMBER')
    if tag:
        version = tag
    else:
        with open('.version') as version_file:
            version = version_file.read().strip()
        if 'rc' in version and build_number:
            version = '{}-{}'.format(version, build_number)
    print('Current Version is: {}'.format(version))
    return version


setup(
    name='sonic-cd',
    version=get_version(),
    author='Tomas Riha',
    author_email='tomas.riha@wirelesscar.com',
    packages=['soniclib'],
    include_package_data=True,
    scripts=['sonic', 'sonic-context'],
    install_requires=[
        'awscli >= 1.16.118',
        'PyYAML <=3.13,>=3.10',
        'boto3 >= 1.9.108',
        'botocore >= 1.12.108',
        'sh >= 1.12.14',
        'python-json-logger >= 0.1.8',
        'validators >= 0.12.4'
    ],
    setup_requires=[
        'nose >= 1.3.7',
        'coverage >= 4.5.2'
    ],
    tests_require=[
        'mock >= 2.0.0',
        'pycodestyle >= 2.4.0'
    ]
)
