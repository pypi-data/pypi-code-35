import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezWxPython",
    version="0.3.8",
    author="zdiv",
    author_email="zdiv@daum.net",
    description="Easy wxPython wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="GUI UI wxpython wrapper simple easy beginner novice student graphics", 
    url="https://github.com/zdivdev/ezWxPython",
    #packages=setuptools.find_packages(),
    packages=[ 'ezWxPython', 'ezWxPython/example' ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)