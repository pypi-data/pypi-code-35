from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

v='0.0.3'

setup(
    name='pyparsers',
    version=v,
    packages=['pyparsers', 'pyparsers.CYK'],
    url='https://github.com/PatrikValkovic/pyparsers',
    license='GNU General Public License v3.0',
    download_url='https://github.com/PatrikValkovic/pyparsers/archive/v' + v + '.tar.gz',
    author='Patrik Valkovic',
    author_email='patrik.valkovic@hotmail.cz',
    description='Parsers for grammpy library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'grammpy'
    ]
)
