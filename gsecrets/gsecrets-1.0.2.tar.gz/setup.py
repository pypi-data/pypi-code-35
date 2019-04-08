from setuptools import find_packages, setup, Command
import os
import sys
from shutil import rmtree

here = os.path.abspath(os.path.dirname(__file__))

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        sys.exit()

setup(name='gsecrets',
      version='1.0.2',
      description='API and CLI for securely managing secrets',
      url='https://github.com/openeemeter/gsecrets',
      author='Open Energy Efficiency',
      packages=find_packages(),
      install_requires=[
        'click',
        'google-api-python-client',
        'google-cloud-storage',
        'ndg-httpsclient',
        'pyasn1',
        'pyopenssl',
        'requests',
      ],
      entry_points={  
        'console_scripts': [  
          'gsecrets = gsecrets.cli:cli',  
        ] 
      },
      cmdclass={
        'upload': UploadCommand,
      },
)