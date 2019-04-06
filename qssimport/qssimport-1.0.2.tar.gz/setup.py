import os
from functools import wraps

from setuptools import setup
from qssimport import version


def read(file_name):
    f = open(os.path.join(os.path.dirname(__file__), file_name)).read()
    return f


setup(
    name='qssimport',
    version=version.__version__,
    author='Chris Souza',
    author_email='chris.souza3425@gmail.com',
    python_requires='>=3.4',
    description="Merge qss files by using @import",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/c385/qssimport",
    license='MIT',
    packages=['qssimport'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        ],
    )


