# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from link_migration.framework.version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='link_migration',
      version=VERSION,
      description="A generic tool for migrate in python.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      keywords='migration',
      author='Alex Sansone',
      author_email='aeris1987@gmail.com',
      url='https://github.com/takamuffin/link-migration',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'link_migration']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "termcolor"
      ],

      entry_points={
            'console_scripts': [
                'link_migration = link_migration.framework.runner:link_migration',
            ]
        },
      )
