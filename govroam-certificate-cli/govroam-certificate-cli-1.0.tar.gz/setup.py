import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='govroam-certificate-cli',  
     version='1.0',
     author="Mike Richardson",
     author_email="doctor@perpetual.name",
     description="CLI certificate generator for Govroam",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=['govroam_certificate_cli'],
     classifiers=[
         "Programming Language :: Python :: 2",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
         "simple-roaming-certificate"
     ],
 )
 
 