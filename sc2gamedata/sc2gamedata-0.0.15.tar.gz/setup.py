from distutils.core import setup

VERSION = '0.0.15'

setup(
  name='sc2gamedata',
  packages=['sc2gamedata'],
  version=VERSION,
  description='Utility for making queries on the SC2 Game Data API and the SC2 Community API',
  author='Hugo Wainwright',
  author_email='wainwrighthugo@gmail.com',
  url='https://github.com/frugs/sc2api_queries',
  download_url='https://github.com/frugs/sc2api_queries/tarball/' + VERSION,
  keywords=['ladder', 'starcraft', 'sc2', 'api', 'query', 'battle', 'net'],
  classifiers=[],
)
