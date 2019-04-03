from setuptools import setup

with open('./namepy/version.py', 'r') as infile:
    __version__ = infile.readline().split('=')[1].strip().strip("'")


__description__ = 'Command-line tool to generate names for the uncreative'


setup(
    name='namepy',
    author='Marcus Medley',
    author_email='mdmeds@gmail.com',
    license='MIT',
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
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
    )
)
