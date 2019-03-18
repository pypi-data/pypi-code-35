import os
from distutils.core import setup
from setuptools import find_packages

here = os.path.dirname(__file__)
packages = find_packages(where=here)
package_dir = {k: os.path.join(here, k.replace(".", "/")) for k in packages}

setup(name='amlfbp',
      version='0.35',
      description="Azure Machine Learning service compute for Busy People. See more in the Github",
      author='Aleksander Callebat',
      author_email='aleks_callebat@hotmail.fr',
      url='https://github.com/alekscallebat/amlfbp',
      packages=["amlfbp"],
      entry_point={'console_scripts': ['amlfbp = amlfbp.main:main']})