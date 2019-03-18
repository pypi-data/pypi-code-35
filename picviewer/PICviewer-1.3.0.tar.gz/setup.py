import sys
from setuptools import setup, find_packages

# Get the package requirements from the requirements.txt file
with open('./requirements.txt') as f:
    install_requires = [line.strip('\n') for line in f.readlines()]

# Read the version number, by executing the file picviewer/__version__.py
# This defines the variable __version__
with open('./picviewer/__version__.py') as f:
    exec( f.read() )

setup(name='PICviewer',
      version=__version__,
      description='PyQt-based visualization tools for PIC simulations',
      url='https://bitbucket.org/ecp_warpx/picviewer/src/master/',
      author='Jaehong Park',
      author_email='jaehongpark@lbl.gov',
      packages=find_packages('.'),
      package_data={'picviewer': ['ui_files/*.ui',
			  					  'images/*.png']},
      entry_points={
          'console_scripts': [
              'picviewer = picviewer.__main__:launch_gui']},
     install_requires=install_requires,
      )
