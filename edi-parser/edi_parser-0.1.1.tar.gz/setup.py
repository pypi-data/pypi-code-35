from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='edi_parser',
    version='0.1.1',

    description='',
    long_description=long_description,

    url='',

    author='Joao Escudero',
    author_email='joao.escudero@conferecartoes.com.br',

    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Plugins',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='',

    packages=find_packages(exclude=['.git', 'templates']),
)
