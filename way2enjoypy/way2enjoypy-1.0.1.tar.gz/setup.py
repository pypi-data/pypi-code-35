import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'way2enjoypy'))
from version import __version__

install_require = ['requests >= 2.7.0, < 3.0.0']
tests_require = ['nose >= 1.3, < 2.0', 'httpretty >= 0.8.10, < 1.0.0']

if sys.version_info < (2, 7):
    tests_require.append('unittest2')
if sys.version_info < (3, 3):
    tests_require.append('mock >= 1.3, < 2.0')

setup(
    name='way2enjoypy',
    version=__version__,
    description='way2enjoy API client.',
    author='way2enjoy',
    author_email='support@way2enjoy.com',
    license='MIT',
    long_description='Python client for the way2enjoy API. way2enjoy compresses your images intelligently. Read more at https://way2enjoy.com.',
    url='https://way2enjoy.com/developers',

    packages=['way2enjoypy'],
    package_data={
        '': ['LICENSE', 'README.md'],
        'way2enjoypy': ['data/cacert.pem'],
    },

    install_requires=install_require,
    tests_require=tests_require,
    extras_require={'test': tests_require},

    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
