import sys
from setuptools import setup

setup(
    name = "renesy-helloworld",        # what you want to call the archive/egg
    version = "0.1.3",
    packages=["helloworld"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'helloworld[foo]'
    package_data = {},
    author="Robert Sprunk",
    author_email = "renesy@users.noreply.github.com",
    description = "An example program in Python with a multi-stage Docker build",
    license = "GPLv3",
    keywords= "example documentation tutorial",
    url = "https://github.com/renesy/python-docker-multistage-helloworld",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "helloworld_in_python = helloworld.main:main",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
