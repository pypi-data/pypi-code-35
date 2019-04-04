from distutils.core import setup
setup(
  name = 'bulk-renamer',
  packages = ['bulk-renamer'],
  version = '0.2',
  license='MIT',
  description = 'A Python script to bulk renamer files in a directory.',
  author = 'Matthew Kleiner',
  url = 'https://github.com/mrniceguy127/bulk-renamer',
  download_url = 'https://github.com/mrniceguy127/bulk-renamer/archive/v_02.tar.gz',
  keywords = ['bulk', 'renamer', 'renamer', 'files', 'directories'],
  entry_points = {
    "console_scripts": [
      "bulk-renamerr = bulk-renamer.bulk-renamer:run",
    ]
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
