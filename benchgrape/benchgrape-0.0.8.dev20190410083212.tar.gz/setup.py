
from setuptools import setup, find_packages
from benchgrape.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='benchgrape',
    version=VERSION,
    description='This is how you\'d Bench a Grape!',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Riccardo Salzer',
    author_email='beschwerden@salzamt.xyz',
    url='https://gitlab.chatgrape.com/salzamt/benchgrape',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'benchgrape': ['templates/*']},
    install_requires=[
        'cement==3.0.2', 'locustio', 'websocket-client', 'jinja2', 'pyyaml',
        'colorlog',
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        benchgrape = benchgrape.main:main
    """,
)
