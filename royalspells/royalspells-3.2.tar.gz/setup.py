import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="royalspells",
    version="3.2",
    author="Stefano Pigozzi",
    author_email="ste.pigozzi@gmail.com",
    description="A package to procedurally generate useless spells!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steffo99/royalspells",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires="~=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ]
)
