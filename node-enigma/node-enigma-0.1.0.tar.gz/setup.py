from setuptools import setup , find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='node-enigma',
    version='0.1.0',
    description='Python Command Line to encrypt and decrypt messages',
    url="https://github.com/dyeboah/enigma.py",
    author="David Yeboah",
    author_email="dyeboah@oswego.edu",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Argparse', 'Requests', 
    ],
    entry_points='''
        [console_scripts]
        enigma=script.enigma:main
    ''',
    license=['MIT'],
    keyword= "enigma machine node",
    long_description=long_description,
    long_description_content_type='text/markdown'
    ,
)