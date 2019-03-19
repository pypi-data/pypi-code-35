import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="makegit",
    version="0.80.1",
    author="Anthony Potappel",
    author_email="anthony.potappel@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Merge GIT submodule repositories into a single buildrepo",
    url="https://github.com/LINKIT-Group/makegit",
    packages=setuptools.find_packages(),
    #python_requires='~=3.5, ~=3.6, ~=3.7',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
