import setuptools
from setuptools import find_packages

import gwap_framework


def long_description():
    with open('README.md', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='gwap-framework',
    version=gwap_framework.__version__,

    url='https://gitlab.com/gwap/python/gwap-framework/',
    description='Biblioteca padrão de framework para aplicações em Python no GWAP.',
    long_description=long_description(),
    long_description_content_type="text/markdown",

    author='Guilherme Dalmarco',
    author_email='dalmarco.br@gmail.com',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],

    include_package_data=True,
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'flask',
        'flask-restful',
        'redis',
        'python-decouple',
        'schematics',
        'aiohttp',
        'sqlalchemy',
        'pycryptodome==3.7.3',
        'cffi==1.12.2',
        'pyjwt==1.7.0',
        'cryptography==2.5',
    ],
    extras_require={},
)
