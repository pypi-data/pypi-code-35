#!/usr/bin/python3

from setuptools import setup
# import fastentrypoints


with open('jv/_version.py') as f:
    exec(f.read())

setup(
    name='jv',
    version=__version__,    # noqa: F821

    description="",
    url='',
    license='LGPL-3.0',

    author="Vojtěch Pachol",
    author_email="pacholick@gmail.com",

    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
    ],
    keywords='python',

    packages=['jv'],
    # setup_requires=['fastentrypoints'],
    install_requires=[],

    data_files=[],
    entry_points={
        'console_scripts': [
            'jv=jv:main',
        ],
    },
)
