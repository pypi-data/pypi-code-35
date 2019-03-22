from distutils.core import setup
setup(
  name = 'bconf',         # How you named your package folder (MyLib)
  packages = ['bconf'],   # Chose the same as "name"
  version = '0.15.220319',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple Python configuration manager.',   # Give a short description about your library
  author = 'the_big_cheese',                   # Type in your name
  author_email = 'slendi3@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Mackenzie01/bconf',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Mackenzie01/bconf/archive/0.15.220319.tar.gz',    # I explain this later on
  keywords = ['Management', 'Tool', 'Configuration'],   # Keywords that define your package best
  install_requires = [],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
