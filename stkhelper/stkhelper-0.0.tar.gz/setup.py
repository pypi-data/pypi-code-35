from distutils.core import setup

setup(
      name='stkhelper',
      version='0.0',
      description='Uses the STK software to create simulations for satellite testing',
      author='W. Conor McFerren',
      author_email='cnmcferren@gmail.com',
      packages=['stkhelper'],
      install_requires=[
              'win32api',
              'comtypes'
              ]
)