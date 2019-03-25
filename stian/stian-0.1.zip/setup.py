from distutils.core import setup
setup(
  name = 'stian',
  packages = ['stian'],
  version = '0.1',
  license='MIT License',
  description = 'Fetches weather info from darksky.net.',
  author = 'Darren Duncan',
  author_email = 'darren907@hotmail.co.uk',
  url = 'https://github.com/TheStill/stian',
  download_url = 'https://github.com/TheStill/stian/archive/0.1.tar.gz',
  keywords = ['Weather', 'darksky', 'sun'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
