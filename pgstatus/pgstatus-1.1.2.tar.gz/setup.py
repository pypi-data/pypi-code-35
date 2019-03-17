
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

from setuptools import setup, find_packages
from pgstatus import __version__

setup(
    name='pgstatus',
    keywords='postgresql haproxy status check tools',
    description='HTTP server to check postgresql server status',
    long_description=long_description,
    author='Ilkka Tuohela',
    author_email='ilkka.tuohela@codento.com',
    url='https://github.com/hile/pgstatus/',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    python_requires='>=2.7',
    install_requires=(
        'configobj',
        'psycopg2-binary',
        'systematic',
    ),
    setup_requires=(
        'pytest-runner',
    ),
    tests_require=(
        'pytest',
        'pytest-datafiles',
    ),
    entry_points={
        'console_scripts': [
            'pgstatus-daemon=pgstatus.bin.pgstatus_daemon:main',
        ],
    },
)
