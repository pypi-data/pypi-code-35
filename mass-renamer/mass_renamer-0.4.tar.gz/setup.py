from distutils.core import setup
setup(
  name = 'mass_renamer',
  packages = ['mass_renamer'],
  version = '0.4',
  license='MIT',
  description = 'A Python script to mass rename files in a directory.',
  author = 'Matthew Kleiner',
  url = 'https://github.com/mrniceguy127/mass-renamer',
  download_url = 'https://github.com/mrniceguy127/mass-renamer/archive/v_0.4.tar.gz',
  keywords = ['renamer', 'rename', 'file system'],
  entry_points = {
    "console_scripts": [
      "mass-renamer=mass_renamer.mass_renamer:run",
    ]
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
