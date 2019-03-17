from setuptools import setup

with open('./namepy/version.py', 'r') as infile:
    __version__ = infile.readline().split('=')[1].strip().strip("'")


__description__ = 'Command-line tool to generate names for the uncreative'


setup(
    name='namepy',
    author='Marcus Medley',
    author_email='mdmeds@gmail.com',
    version=__version__,
    description=__description__,
    long_description=__description__,
    packages=['namepy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'namepy = namepy.__main__:main'
        ]
    },
    keywords=['names', 'naming', 'name', 'generator'],
    url='https://github.com/mdmedley/namepy',
)
