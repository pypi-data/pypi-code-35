from setuptools import setup, find_packages

with open("README.md", "r") as fh :
    long_description = fh.read()

setup(
    name = 'game_machine',
    packages = find_packages(),
    version = '0.5',
    description = 'A 2D sprite based game engine/PyGame wrapper',
    url="https://github.com/thismachinekillszombies/game_machine",
    long_description = long_description,
    long_description_content_type = "text/markdown", 
    author = 'Richard Butterworth',
    author_email = 'richard@richardbutterworth.co.uk',
    license = 'MIT',
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Games/Entertainment"
        ],
    install_requires = [
        'pygame',
    ],
    zip_safe=False
)
