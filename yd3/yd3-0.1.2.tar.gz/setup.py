from setuptools import setup
import sys, os

version = '0.1.2'

setup(
    name = 'yd3',
    version = version,
    packages = ['yd3'],
    description = 'bilingual dictionary in command line',
    long_description = 'bilingual dictionary in command line',
    classifier = [],
    author = 'Xuyan Ru',
    author_email = 'lelielru@gmail.com',
    url = 'https://github.com/Tacsy/yd3',
    keywords = ['dictionary', 'chinese', 'command line'],    
    license = 'MIT',
    install_requires = ['colored'],
    entry_points={
        'console_scripts':[
                'yd3 = yd3.yd3:main'
                ],
        },
)
