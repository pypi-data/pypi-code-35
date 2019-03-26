from setuptools import setup

with open("README.md") as fp:
    readme = fp.read()

setup(
    name="osis_book_tools",
    version="1.0.0",
    description="A set of tools for converting between OSIS abbreviations and localized biblical book names",
    include_package_data=True,
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    url="http://api.sermonaudio.com/",
    author="SermonAudio.com",
    author_email="info@sermonaudio.com",
    keywords="bible OSIS SBL",
    license="MIT",
    packages=["osis_book_tools"],
)
