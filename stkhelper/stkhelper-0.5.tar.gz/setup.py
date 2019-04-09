from distutils.core import setup

setup(
      name='stkhelper',
      version='0.5',
      description='Uses the STK software to create simulations for satellite testing',
      long_description=open('README.md','r').read(),
      author='W. Conor McFerren',
      author_email='cnmcferren@gmail.com',
      url="https://github.com/cnmcferren/stkhelper",
      packages=['stkhelper'],
      install_requires=[
          'comtypes',
          'win32api']
)
