"""An AWS utility package"""
import setuptools
import lambida

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='lambida',  
     version='0.2.16',
     author="AMARO",
     author_email="data@amaro.com",
     description="An AWS utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url=None,
     install_requires =['boto3==1.9.112',
                        'botocore==1.12.112',
                        's3transfer==0.2.0',
                        'jmespath==0.9.4',
                        'docutils==0.14',
                        'urllib3==1.24.1',
                        'python-dateutil==2.8.0',
                        'six==1.12.0'],
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
