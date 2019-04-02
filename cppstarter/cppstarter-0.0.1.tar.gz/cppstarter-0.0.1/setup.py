import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='cppstarter',  
     version='0.0.1',
     scripts=['cppstarter'] ,
     author="Wan Song",
     author_email="wansong@sina.cn",
     description="create cpp project cmake googletest unittest",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/bestofsong/cpp-starter",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
