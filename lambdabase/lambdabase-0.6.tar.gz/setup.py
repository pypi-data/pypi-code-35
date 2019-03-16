import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='lambdabase',
    version='0.6',
    scripts=[],
    author='Daniel Bardsley',
    author_email='daniel@bardsley.org.uk',
    decription='A library to support development of enterprise Serverless applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/danielbardsley/lambdabase',
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 2.7",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"
     ]
)
