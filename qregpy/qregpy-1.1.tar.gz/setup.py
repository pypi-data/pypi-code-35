# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='qregpy',
    version='1.1',
    description='Query-centric regression model.',
    classifiers=[
        'Development Status :: 1.0',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Approximate Query Processing :: Regression :: ensemble method',
      ],
    keywords='Query-centric Regression',
    url='https://github.com/qingzma/QReg',
    author='Qingzhi Ma',
    author_email='Q.Ma.2@warwick.ac.uk',
    long_description=readme,
    license=license,
    packages=['qregpy'],#find_packages(exclude=('tests', 'docs','results'))
    zip_safe=False,
    install_requires=[
          'xgboost','numpy','scikit-learn'
      ],
    test_suite='nose.collector',
    tests_require=['nose'],
)

