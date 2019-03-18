from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='eppzy',
    description='EPP Client Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['epp'],
    url='https://gitlab.com/aaisp/eppzy',
    author='David Honour',
    author_email='david@concertdaw.co.uk',
    version='0.0.1',
    license='LGPL3',
    packages=['eppzy'],
    install_requires=[
    ],
    extras_require={
        'test': ['pytest-flake8', 'mock']
    },
    entry_points={}
)
