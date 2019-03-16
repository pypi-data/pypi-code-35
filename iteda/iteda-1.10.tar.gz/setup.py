#from distutils.core import setup
from setuptools import setup

#f = open('README.md')


setup(
  name = 'iteda',         # How you named your package folder (MyLib)
  packages = ['iteda'],   # Chose the same as "name"
  version = '1.10',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a menu to control an integrating sphere through a serial interface (rs232)',   # Give a short description about your library
  #long_description=read('README.rst'),
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  author = 'victor esparza',                   # Type in your name
  author_email = 'vicmaresparza@gmail.com',      # Type in your E-Mail
  url = 'https://gitlab.com/fabriziodifran/esfera-codigo-verilog',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['MENU', 'UART', 'SPHERE'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
          'numpy',
          'pyserial',
          'argparse',
          'serial',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',      #Specify which pyhton versions that you want to support
  ],
)