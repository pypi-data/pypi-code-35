from setuptools import setup

setup(
    name='plantpredict',
    version='0.8.3',
    description='Python 2.7 SDK for PlantPredict (https://ui.plantpredict.com).',
    url='http://github.com/storborg/funniest',
    author='Stephen Kaplan, Performance & Prediction Engineer at First Solar, Inc.',
    author_email='stephen.kaplan@firstsolar.com',
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    packages=['plantpredict'],
    install_requires=[
        'requests==2.21.0',
        'pandas==0.24.2',
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'idna==2.8',
        'numpy==1.16.2',
        'python-dateutil==2.8.0',
        'pytz==2018.9',
        'six==1.12.0',
        'urllib3==1.24.1'
    ]
)
