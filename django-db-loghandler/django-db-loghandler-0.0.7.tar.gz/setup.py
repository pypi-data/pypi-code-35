from setuptools import setup
from db_loghandler import __version__

description = "Logging handler for Django Database"
long_description = description
install_requires=[
    'django >= 1.2.7',
]

setup(
    name='django-db-loghandler',
    version=__version__,
    description=description,
    author='Jonghak Choi',
    author_email='haginara@gmail.com',
    long_description=long_description,
    packages=['db_loghandler', 'db_loghandler.migrations'],
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
