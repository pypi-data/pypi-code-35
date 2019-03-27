import pathlib
from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'hrpy',         # How you named your package folder (MyLib)
  packages = ['hrpy'],   # Chose the same as "name"
  version = '0.0.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'hr but written in python',   # Give a short description about your library
  long_description = README, 
  long_description_content_type = "text/markdown",
  author = 'John Naylor',                   # Type in your name
  author_email = 'jonaylor89@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jonaylor89/hrpy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jonaylor89/hrpy/archive/v_0.8.tar.gz',    # I explain this later on
  keywords = ['hr', 'terminal', 'formatting'],   # Keywords that define your package best
  entry_points={"console_scripts": ["hr=hrpy.hr:main"]},
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
