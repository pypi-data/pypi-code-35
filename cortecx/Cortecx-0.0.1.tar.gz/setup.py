from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='Cortecx',
      version=version,
      description="Cortecx is a Deep Learning ToolKit",
      long_description=open('README.txt').read(),
      classifiers=[],
      keywords='artificial intelligence',
      author='Lleyton Ariton',
      author_email='lleyton.ariton@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
