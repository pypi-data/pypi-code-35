import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='LTRI-Funcs-knamdar',

     version='0.0.8',

     author="Khashayar Namdar",

     author_email="knamdar@uwo.ca",

     description="Handy functions used in LTRI Machine Learning Lab",

     long_description=long_description,

     long_description_content_type = "text/markdown",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
