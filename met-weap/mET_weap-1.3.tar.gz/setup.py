# -*- coding: utf-8 -*-
"""
Created on Mon May  7 12:09:54 2018

@author: VI
"""

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='mET_weap',
    version='1.3',
    description='ERA5/MODIS Preprocessor for WEAP 21',
    long_description=long_description,
	long_description_content_type='text/markdown',
#   url='https://github.com/pypa/sampleproject', 
    author='Michel Le Page, Cindy Gosset, Antoine Beaumont, CESBIO',  
    author_email='michel.lepage@cesbio.cnes.fr', 
    classifiers=[  
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
		'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
    install_requires=['numpy>="1.11.3"','pillow>="3.4.2"','xlrd>="1.0.0"','scipy>="0.19.1"','ecmwf-api-client>="1.4.2"','requests>="2.14.2"','python-dateutil>="2.4"','cdsapi>="0.1.1"','netCDF4>="1.4.1"'],                                      
	packages= ['mET_weap','mET_weap.mET_weap_doc','mET_weap.mET_weap_test','mET_weap.Tab_ndvi_kc_fc','mET_weap.mET_weap_test.Gtopo30','mET_weap.mET_weap_test.Tab_ndvi_kc_fc','mET_weap.mET_weap_test.zonage'],
	package_data={
        # If any package contains these extensions, include them:
        '': ['*.txt', '*.rst','*xlsx','*.pdf','*.md','*.cpg','*.dbf','*.prj','*.sbn','*.sbx','*.shp','*.shp.xml','*.shx'],
    }
) 