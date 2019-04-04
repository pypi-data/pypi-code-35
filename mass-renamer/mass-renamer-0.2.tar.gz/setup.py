from distutils.core import setup
setup(
  name = 'mass-renamer',
  packages = ['mass-renamer'],
  version = '0.2',
  license='MIT',
  description = 'A Python script to mass renamer files in a directory.',
  author = 'Matthew Kleiner',
  url = 'https://github.com/mrniceguy127/mass-renamer',
  download_url = 'https://github.com/mrniceguy127/mass-renamer/archive/v_02.tar.gz',
  keywords = ['mass', 'renamer', 'renamer', 'files', 'directories'],
  entry_points = {
    "console_scripts": [
      "mass-renamer=mass-renamer.mass-renamer:run",
    ]
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
