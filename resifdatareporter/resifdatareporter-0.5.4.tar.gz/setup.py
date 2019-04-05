from io import open
from setuptools import setup, find_packages

with open('resifdatareporter/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='resifdatareporter',
    version=version,
    description='Scans the resif data repository and compute metrics. Sends the result in influxdb or postgres',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Jonathan Schaeffer',
    author_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    maintainer='Jonathan Schaeffer',
    maintainer_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    url='https://gricad-gitlab.univ-grenoble-alpes.fr/OSUG/RESIF/resif_data_reporter',
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[
        'Click==7.0',
        'python-dateutil==2.7.5',
        'PyYAML==5.1',
        'psycopg2-binary==2.7.6.1',
        'influxdb==5.2.1',
    ],
    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ],

    tests_require=['coverage', 'pytest'],
    entry_points='''
    [console_scripts]
    resifdatareporter=resifdatareporter.resifdatareporter:cli
    '''
)
