import multiprocessing
from setuptools import setup

with open('README.md', 'r') as readme:
    desc = readme.read()

setup(name = 'evepy',
    version = '2.1',
    py_modules = ['eve'],
    author = 'Munchii',
    author_email = 'contact@munchii.me',
    license = 'MIT',
    description = 'Simple lightweight data-interchange format, written in Python',
    long_description = desc,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Dmunch04/EVE',
    classifiers = [
            'Development Status :: 4 - Beta',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
    ],
    keywords = 'simple data interchange format python'
    )
