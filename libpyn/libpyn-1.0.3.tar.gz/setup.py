import setuptools
from os import path

dir = path.abspath(path.dirname(__file__))

with open(path.join(dir, 'README.md'), 'r') as f:
    desc = f.read()

requirements = ['beautifulsoup4', 'lxml', 'requests']

setuptools.setup(
      name='libpyn',
      version='1.0.3',
      description='Libsyn podcast API',
      long_description=desc,
      long_description_content_type='text/markdown',
      install_requires=requirements,
      url='https://github.com/RobbyB97/libpyn',
      author='Robby Bergers',
      author_email='bergersr@my.easternct.edu',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False
)
entry_points={
    '__init__': [
        'menu = libpyn.podcast:gen',
    ],
},
