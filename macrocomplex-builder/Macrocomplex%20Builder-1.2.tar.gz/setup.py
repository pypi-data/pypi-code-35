#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup


setup(name='Macrocomplex Builder',
	version='1.2',
	description='This program is able to reconstruct biological macrocomplexes of protein-protein interactions as well as protein-DNA/RNA interactions given a set of binary interactions and the desired number of chains of the target complex.',
	author='Guillermo Palou Marquez and Javier Sanchez Utges',
	author_email='guillepalou4@gmail.com',
	#packages=['macrocomplex_builder'],
	url='https://github.com/gpalou4/macrocomplex_builder',
	#py_modules=[''],
	scripts=['macrocomplex_builder.py','macrocomplex_functions.py'])




# it looks for the the modules in the "root" package, if there are not there, specify a package_dir option
# package_dir = {'': 'lib'}

# To create a source distribution for this module, run this on the terminal
# python setup.py sdist
# this will create an archive file (tarball/ZIP) containing the setup script and the specified modules.

# if and end user whises to install your module, has to download the tar file, unpack it, and from the directory created run:
# python setup.py install