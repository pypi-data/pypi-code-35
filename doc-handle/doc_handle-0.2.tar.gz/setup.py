import setuptools

with open("README.md", 'r') as f:
     long_description = f.read()

setuptools.setup(
   name='doc_handle',
   version='0.2',
   description='doc_handle a python module for working with .csv and .ods in python native',
   long_description=long_description,
   license="LICENSE",
   author='Javier Cabau Laporta',
   author_email='jcabaulaporta@outlook.es',
   install_requires=['numpy>=1.16.2', 'pyexcel>=0.5.13', 'pyexcel-ods>=0.5.6'],
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
      "Operating System :: OS Independent",
   ],
)
