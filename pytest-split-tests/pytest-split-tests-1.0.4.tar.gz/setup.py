import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name="pytest-split-tests",
    description=('A Pytest plugin for running a subset of your tests by '
                 'splitting them in to equally sized groups. Forked from '
                 'Mark Adams\' original project pytest-test-groups.'),
    url='https://github.com/wchill/pytest-split-tests',
    author='Eric Ahn',
    author_email='wchill@chilly.codes',
    packages=['pytest_split_tests'],
    version='1.0.4',
    long_description=read('README.rst'),
    install_requires=['pytest>=2.5'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Testing',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'
                 ],
    entry_points={
        'pytest11': [
            'split-tests = pytest_split_tests',
        ]
    },
)
