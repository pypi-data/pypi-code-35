from distutils.core import setup
setup(
  name = 'arkouda',         # How you named your package folder (MyLib)
  packages = ['arkouda'],   # Chose the same as "name"
  version = '0.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A numpy replacement backed by Chapel',   # Give a short description about your library
  author = 'Michael Merrill',                   # Type in your name
  url = 'https://github.com/mhmerrill/arkouda',   # Provide either the link to your github or to your website
  install_requires=[            # I get to this in a second
          'h5py',
          'zmq',
      ],
  classifiers=[
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
