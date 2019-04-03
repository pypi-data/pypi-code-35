from distutils.core import setup
setup(
  name = 'thecatapi',
  packages = ['thecatapi'],
  version = '1.1',
  license='MIT',
  description = 'Python3 wrapper for TheCatAPI',
  author = 'Your name',
  author_email = 'your.email@address.com',
  url = 'https://github.com/kevinroleke/thecatapi-wrapper',
  download_url = 'https://github.com/kevinroleke/thecatapi-wrapper/archive/v1.0.tar.gz',
  keywords = ['thecatapi'],
  install_requires=[
          'requests', 'python-magic-bin'
      ],
  classifiers=[
    'Programming Language :: Python :: 3'
  ],
)
