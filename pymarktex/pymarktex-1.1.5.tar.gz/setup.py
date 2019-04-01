from setuptools import setup

setup(
    name             = 'pymarktex',
    version          = '1.1.5',
    description      = 'Will convert a markdown text file to a fancy PDF document',
    license          = 'MIT',
    url              = 'http://github.com/xapple/pymarktex/',
    author           = 'Lucas Sinclair',
    author_email     = 'lucas.sinclair@me.com',
    packages         = ['pymarktex', 'pymarktex.figures', 'pymarktex.templates'],
    scripts          = ['scripts/pymarktex'],
    install_requires = ['autopaths', 'plumbing', 'sh', 'pystache'],
    long_description = open('README.md').read(),
)