import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
      name='stkhelper',
      version='0.4',
      description='Uses the STK software to create simulations for satellite testing',
      long_description=long_description,
      author='W. Conor McFerren',
      author_email='cnmcferren@gmail.com',
      url="https://github.com/cnmcferren/stkhelper",
      packages=setuptools.find_packages(),
      install_requires=[
          'comtypes',
          'win32api']
)
