import os
import sys
from setuptools import setup, find_namespace_packages

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hawkei'))
from version import VERSION

with open('README.md', 'r') as fh:
    long_description = fh.read()

install_requires = [
    'requests>=2',
    'backoff>=1.8',
]

tests_require = [
    'pytest>=4',
]

setup(
    name='hawkei',
    version=VERSION,
    url='https://github.com/hawkei-io/hawkei-python',
    author='Hawkei',
    author_email='support@hawkei.io',
    maintainer='Hawkei',
    maintainer_email='support@hawkei.io',
    packages=find_namespace_packages(include=['hawkei', 'hawkei.*']),
    license='MIT License',
    install_requires=install_requires,
    tests_require=tests_require,
    description='Hawkei python integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
