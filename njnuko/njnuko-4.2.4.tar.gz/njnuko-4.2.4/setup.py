from setuptools import setup, find_namespace_packages
import sys, os

with open("README.md","r") as fh:
      long_description=fh.read()



setup(name="njnuko",
      version="4.2.4",
      description="njnuko tools",
      classifiers=[], 
      author='njnuko',
      author_email='njnuko@163.com',
      url='https://github.com/njnuko/njnuko',
      license='MIT',
      packages=find_namespace_packages(include=['nas.*']),
      include_package_data=True,
      install_requires=['psycopg2','pymysql','filetype'],
      entry_points="",
      )
