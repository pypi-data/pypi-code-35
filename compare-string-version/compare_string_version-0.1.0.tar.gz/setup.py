import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
  name = 'compare_string_version',         # How you named your package folder (MyLib)
  packages=[ 'compare_string_version' ], 
  version = '0.1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'accepts 2 version string as input and returns whether one is greater than, equal, or less than the other',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Miguel Almeida',                   # Type in your name
  author_email = 'mplabdev@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/miguelluiz/compare_string_version',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/miguelluiz/compare_string_version/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Compare', 'version control', 'version string as input'],   # Keywords that define your package best
  install_requires=[],           # I get to this in a second
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Internationalization',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ]
)