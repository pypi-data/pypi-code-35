from setuptools import setup, find_packages
import sys, os


with open("README.md","r") as fh:
      long_description=fh.read()



setup(name="njnuko",
      version="4.2.6",
      description="njnuko tools",
      long_description=long_description,
      classifiers=[], 
      keywords='files sorting',
      author='njnuko',
      author_email='njnuko@163.com',
      url='https://github.com/njnuko/njnuko',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['psycopg2-binary','pymysql','filetype','Pillow'],
      entry_points="",
      )
