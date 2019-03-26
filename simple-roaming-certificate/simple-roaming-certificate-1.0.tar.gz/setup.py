import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='simple-roaming-certificate',  
     version='1.0',
     author="Mike Richardson",
     author_email="doctor@perpetual.name",
     description="Simple certificate generator",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=['simple_roaming_certificate'],
     classifiers=[
         "Programming Language :: Python :: 2",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
         "cryptography"
     ],
 )
 
 