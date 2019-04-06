import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gameit",
    version="0.0.1",
    author="Daniel Peach",
    author_email="dpeachesdev@gmail.com",
    description="An opinionated way to build great games in Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djpeach/Gameit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)

"""" To upload to pypi: 

* Change the version number
* cd into pipenv environment
* run `python setup.py sdist bdist_wheel`
* run `python -m twine upload dist/*`

"""
