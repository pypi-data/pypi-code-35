import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='indiazipcode',  
     version='1.1.3',
     scripts=['indiazipcode'] ,
     author="shriganesh kolhe",
     author_email="shriganeshkaialsh.kolhe@ucdenver.edu",
     description="India PIN/ZIP code utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/ganeshkolhe4392/indiazipcode",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )