import os
import sys
import codecs
from setuptools import setup


tests_require = [
    'pytest',
    'pytest-mock',
]

if sys.version_info < (3, 0):
    tests_require.append('mock')


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='stingconf',
    version='0.0.2',
    author='',
    author_email='',
    maintainer='rsp9u',
    maintainer_email='gctwt852@yahoo.co.jp',
    license='MIT',
    url='https://github.com/rsp9u/stingconf',
    description='Layered configuration library',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=['stingconf'],
    install_requires=[
        'PyYAML',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=tests_require,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
