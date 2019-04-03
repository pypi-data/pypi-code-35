from setuptools import setup

setup(name='powerbirefreshmanual',
      version='0.0.1',
      description='Script for refreshing manual Power BI workbooks',
      url='https://github.com/jor3stuar1/powerbirefreshmanual',	  
      author='Jorge Alvarez',
      author_email='jor3stuar1@gmail.com',
      license='apache2.0',
      packages=['powerbirefreshmanual'],
      install_requires=[
          'pywinauto',
          'psutil'
      ],
	  entry_points = {
        "console_scripts": ['powerbirefreshmanual = powerbirefreshmanual.powerbirefreshmanual:main']
        },
      zip_safe=False)