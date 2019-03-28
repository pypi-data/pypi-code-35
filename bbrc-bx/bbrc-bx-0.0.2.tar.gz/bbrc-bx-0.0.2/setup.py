from distutils.core import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
  name = 'bbrc-bx',
  install_requires=requirements,
  scripts=['bin/bx'],
  version = '0.0.2',
  description = 'BarcelonaBeta + XNAT = bx',
  author = 'Greg Operto',
  author_email = 'goperto@barcelonabeta.org',
  url = 'https://gitlab.com/xgrg/bx',
  download_url = 'https://gitlab.com/xgrg/bx/-/archive/v0.0.2/bx-v0.0.2.tar.gz',
  classifiers = ['Intended Audience :: Science/Research',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering',
      'Operating System :: Unix',
      'Programming Language :: Python :: 3.7' ]
)
