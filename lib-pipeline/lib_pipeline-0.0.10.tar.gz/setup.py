from setuptools import setup, find_packages

setup(
    name="lib_pipeline",
    version="0.0.10",
    author="Blake Lassiter",
    author_email="blakelass@gmail.com",
    description="A python implementation of services to help deploy using aws and terraform",
    url="https://github.com/balassit/lib_pipeline",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)
