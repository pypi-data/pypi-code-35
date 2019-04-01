from setuptools import setup, find_packages

from gimme_cached_property import __version__

setup(
    name='gimme_cached_property',

    version=__version__,

    packages=find_packages(),

    url='https://github.com/MichaelKim0407/gimme-cached-property',

    license="MIT",

    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    classifiers=[
        "Development Status :: 5 - Production/Stable",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",

        "Topic :: Software Development :: Libraries",
    ]
)
