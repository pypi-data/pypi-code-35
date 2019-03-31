import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minipush",
    version="0.0.5",
    author="Rémi 'Mr e-RL'LANGDORPH",
    author_email="r.langdorph@gmail.com",
    description="A package to minimize your scripts and stylesheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merlleu/minipush",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
