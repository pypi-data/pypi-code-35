import setuptools

setuptools.setup(
    name="snakeway",
    version="0.0.4b",
    author="Piotr Karkut",
    author_email="karkucik@gmail.com",
    description="Simple python request profiler",
    long_description="TODO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "jinja2"
    ],
    include_package_data=True
)
