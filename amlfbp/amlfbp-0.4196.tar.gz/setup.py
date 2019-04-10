import os
from setuptools import setup


setup(name='amlfbp',
      version='0.4196',
      description="Azure Machine Learning service compute for Busy People. See more in the Github",
      author='Aleksander Callebat',
      author_email='aleks_callebat@hotmail.fr',
      url='https://github.com/alekscallebat/amlfbp',
      install_requires=["azureml-sdk"],
      packages=["amlfbp"],
      scripts=["amlfbp/config.py","amlfbp/helpers.py"],
      entry_points={ 
            'console_scripts': [
                  'amlfbp = amlfbp.__main__:main',

      ]}
      )