import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NuEdit",
    version="0.0.1",
    author="Nicolai Søborg",
    author_email="nuedit-pip@xn--sb-lka.org",
    description="NuEdit a TUI ontop of Xi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NicolaiSoeborg/pyxit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Editors",
    ],
)
