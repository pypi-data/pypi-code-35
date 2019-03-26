import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'lightlyse',         # How you named your package folder (MyLib)
  packages = ['lightlyse'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Some of the API of the lyse package without the GUI.',   # Give a short description about your library
  author = 'Fred Jendrzejewski',                   # Type in your name
  author_email = 'fred.jendrzejewski@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/synqs/lightlyse',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/synqs/lightlyse/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['labscriptsuite', 'python', 'data-analysis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'atomicwrites', 'attrs', 'certifi', 'h5py', 'more-itertools', 'numpy',
          'pluggy', 'py', 'pytest', 'six', 'virtualenv'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
  ],
)
