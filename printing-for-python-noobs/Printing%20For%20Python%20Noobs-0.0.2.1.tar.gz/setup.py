from setuptools import setup

__project__ = "Printing For Python Noobs"
__version__ = "0.0.2.1"
__description__ = "Printing Program for non coders (:"
__packages__ = ["Printing For Noobs"]

RM = 'README.md'
f = open(RM)
long_description = f.read()
    
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)
