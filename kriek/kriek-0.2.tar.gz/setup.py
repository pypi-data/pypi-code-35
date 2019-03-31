import sys
from setuptools import setup, find_packages

import kriek

setup(
    # package information
    name='kriek',
    version=kriek.__version__,
    description='Fast and simple WSGI-framework to develop restoring api.',
    long_description=kriek.__doc__,
    long_description_content_type="text/markdown",
    author=kriek.__author__,
    author_email='sledeunf@gmail.com',
    url='http://kriek.sylvan.ovh/',
    license='MIT',
    platforms='any',

    # package content
    entry_points = {
        "console_scripts": [
            "kriek = kriek.cli:cli",
        ]
    },
    packages = find_packages(),
    include_package_data = True,
    
    # package dependencies
    install_requires = [
        "python-magic",
        "Werkzeug"
    ]
)
