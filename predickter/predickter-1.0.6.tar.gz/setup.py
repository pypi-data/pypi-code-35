from setuptools import setup
setup(
  name = 'predickter',
  packages = ['predickter'], 
  version = '1.0.6',
  description = 'A library used for live cricket scores from cricbuzz',
  author = 'dilipbobby',
  author_email = 'dilipreddykiralam@gmail.com',
  license = 'MIT',
  url = 'https://github.com/dilipbobby/predickter', 
  download_url = 'https://github.com/dilipbobby/predickter/tarball/1.0.6', 
  keywords = ['cricket', 'cricbuzz','live cricket scores','live cricket'], 
  install_requires=[
          'requests',
      ],
  classifiers = [],
)
