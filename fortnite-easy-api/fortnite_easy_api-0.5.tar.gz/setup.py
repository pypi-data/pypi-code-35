from distutils.core import setup
setup(
  name = 'fortnite_easy_api',
  packages = ['fortnite_easy_api'],
  version = '0.5',
  license='MIT',
  description = 'A simple python library for developers and beginners to easily use difficult apis',
  author = 'OsOmE1',
  author_email = 'gamerosome@gmail.com',
  url = 'https://github.com/OsOmE1/fortnite-easy-api',
  download_url = 'https://github.com/OsOmE1/fortnite_easy_api/archive/0.5.tar.gz',
  keywords = ['python', 'fortnite', 'api'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)