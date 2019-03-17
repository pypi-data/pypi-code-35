from setuptools import setup

long_description = """\
For authors of command-line utilities. Simplifies: 1) Defining command-line options
and parameters, 2) Parsing the command line, and 3) Displaying usage instructions
to the console.

Utility developers will 1) Subclass a module-defined class, 2) Include a YAML spec
in the subclass to define the utility's options and usage, and 3) Invoke the module
arg parser. When the utility is run, if the command line is valid according to 
the YAML schema, then the supplied args are injected into the subclass by the
parser. Otherwise errors are automatically displayed to the console.

If the user specifies '-h' or '--help' on the command line, then usage instructions
are displayed as defined in the YAML, in a form generally recognizable to users
of console utilities. Specifically, displays summary usage, detailed options and
params (including categorized options), positional params, and examples.
"""

setup(
    name="pycmdparse",
    version="1.0.0",
    description="A Python command line arg parser, and usage instructions generator",
    long_description=long_description,
    url="https://github.com/aceeric/pycmdparse",
    author="Eric Ace",
    author_email="ericace@protonmail.com",
    license="Public Domain",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="arg argument parse command line usage instructions console utility",
    packages=['pycmdparse'],
    install_requires=['PyYAML==5.1b3'],
    python_requires='~=3.6',
)
