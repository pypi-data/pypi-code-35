import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shipmnts-utils",
    version="0.0.1",
    author="Vimox Shah",
    author_email="vimox@shipmnts.com",
    description="Shipmnts Utility Functions",
    long_description_content_type="text/markdown",
    install_requires=["Django==2.1.4"],
    url="https://github.com/vimox-shah/shipmnts_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)