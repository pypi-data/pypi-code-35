"""Setup file for the cryptoaddress library"""
import os

from setuptools import find_packages, setup


def _read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding='utf8') as file:
        return file.read()


setup(
    name='cryptoaddress',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Jose Molina Colmenero',
    author_email='molina@bity.com',
    description='Python library to verify crypto addresses.',
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
    test_suite='tests',
    zip_safe=False
)
