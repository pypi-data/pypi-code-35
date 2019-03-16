import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='brainfuckmachine',  

     version='0.1.1.3',

     scripts=['brainfuckmachine'],

     author="Vlad Havrilov",

     author_email="wladgavrilov@gmail.com",

     description="Simple Brainfuck compiler for python",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://bitbucket.org/schrodenkatzen/brainfuckmachine/src/master/",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
