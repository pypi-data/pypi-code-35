
from setuptools import setup, find_packages
from pgstatus import __version__

setup(
    name='pgstatus',
    keywords='postgresql haproxy status check tools',
    description='HTTP server for haproxy to check postgresql server status',
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
