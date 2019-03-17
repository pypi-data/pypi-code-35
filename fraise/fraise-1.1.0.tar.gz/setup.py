from setuptools import setup, find_packages

setup(name='fraise',
      version='1.1.0',
      description='Generate memorable pass phrases',
      url='http://github.com/daveygit2050/fraise',
      author='Dave Randall',
      author_email='dave@goldsquare.co.uk',
      license='Apache v2',
      packages=find_packages(exclude=('tests', 'docs', 'target')),
      zip_safe=False)
