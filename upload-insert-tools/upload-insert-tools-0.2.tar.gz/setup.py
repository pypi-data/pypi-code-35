from setuptools import setup

setup(name='upload-insert-tools',
      version='0.2',
      description='upload log to flask logger',
      url='https://flask-logger.herokuapp.com/',
      author='Gal Metzer / Dor Genosar',
      author_email='gal.metzer@gmail.com',
      license='apache',
      packages=['upload-insert-tools'],
      install_requires=['requests'],
      zip_safe=False)
