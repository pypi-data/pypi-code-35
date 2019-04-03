from setuptools import setup
from networktools.requeriments import read

requeriments = read()

setup(name='gnsocket',
      version='0.1',
      description='GPS Network Socket, with asyncio stream manager',
      url='http://gitlab.csn.uchile.cl/dpineda/gus',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      install_requires=requeriments,
      packages=['gnsocket'],
      zip_safe=False)
