import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "SQLtills",
    version = "0.0.3",
    author = "Omar Nasr",
    author_email = "omardev9898@gmail.com",
    description = "Simple CRUD utilities for sqlalchemy",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Moro-Code/sqltills",
    license = "MIT",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    install_requires = [
        'SQLAlchemy==1.3',
    ],
    
)