import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Flask-Performance",
    version="0.0.2",
    author="Spacebox(盒子空间) Team",
    author_email="spacebox@spacebox.fun",
    description="A Flask extension to monitoring every api request performance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SpaceBoxer/flask-performance",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
