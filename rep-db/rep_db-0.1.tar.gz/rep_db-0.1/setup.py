import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name="rep_db",  
     version="0.1",
     scripts=["install"] ,
     author="Ryan Guild",
     author_email="ryanguild489@gmail.com",
     description="a SQLAlchemy helper package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/RyanGuild/REP-flask-boilerplate",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
