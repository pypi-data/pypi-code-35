import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='equation_cipher',
     version='0.0.2',
     author="Shounak Joshi",
     author_email="shounakjoshi16@gmail.com",
     description="An Encryption algorithm for encrypting ay text.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://gitlab.com/malhar_stories/equeation_cipher",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
