"""Setup script for Qonstellation Client"""

import os.path
from setuptools import setup


# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, 'README.md')) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name='qonstellation',
    version='0.1.0',
    description='Qonstellation Client',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/qonstellation/client',
    author='Qonstellation LLC',
    author_email='support@qonstellation.co',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=['qonstellation'],
    include_package_data=True,
    install_requires=[
        'feedparser', 'html2text', 'importlib_resources', 'typing'
    ],
    entry_points={'console_scripts': ['qonstellation=reader.__main__:main']},
)
