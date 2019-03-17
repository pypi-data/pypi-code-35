import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tiquations",
    version="0.0.8",
    author="Tinos Psomadakis",
    author_email="tinosps@gmail.com",
    description="A package that solves important formulas for physics and mathematics. Head to the website for documentation and more info!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://tinosps.wixsite.com/tiquations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
            ],
)
