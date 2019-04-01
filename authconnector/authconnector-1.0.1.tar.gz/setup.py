import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='authconnector',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GNU Public License',
    description='This project contains the basic authentication against the remote JWT service.',
    long_description=README,
    url='https://github.com/Tibiritabara/django-auth-connector.git',
    author='Ricardo Santos',
    author_email='ricardo.santos.diaz@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "Django >= 2.1.0",
        "djangorestframework >= 3.8.2",
        "requests >= 2.19.1",
    ]
)
