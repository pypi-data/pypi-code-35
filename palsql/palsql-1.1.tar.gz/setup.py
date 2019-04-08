from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='palsql',
      version='1.1',
      description='Sqlite3 Wrapper Class',
      long_description=long_description,
      url='https://github.com/ipal0/palsql',
      author='Pal',
      author_email='ipal0can@gmail.com',
      license='GPL',
      python_requires='>=3',
      packages=['palsql'])
