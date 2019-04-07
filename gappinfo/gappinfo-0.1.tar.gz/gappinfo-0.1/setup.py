
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='gappinfo',  
     version='0.1',
     scripts=['gappinfo'] ,
     author="Gautham Prakash",
     author_email="gauthamp10@gmail.com",
     description="Google App Information Tool",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/gauthamp10/Google_Play_App_Info",
     packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4==4.7.1',
        'requests',
        'bs4',
    ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    keywords='google apps android'
 )
