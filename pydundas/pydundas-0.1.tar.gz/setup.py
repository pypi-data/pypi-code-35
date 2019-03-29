import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    # 1) All lines in requirements .txt...
    y for y in
    # 3) .. after removing comments and whitespaces.
    [re.sub(r'\s*#.*', '', x).strip() for x in open('requirements.txt').readlines()]
    # 2) ... which are note empty...
    if y
]

setuptools.setup(
     name='pydundas',
     version='0.1',
     license='MIT',
     scripts=['example.py'] ,
     author="Guillaume Roger",
     author_email="guillaume@lomig.net",
     description="Manage sessions for Dundas api.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/lomignet/pydundas",
     packages=setuptools.find_packages(),
     install_requires=requirements,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
