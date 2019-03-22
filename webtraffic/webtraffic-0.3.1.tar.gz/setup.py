import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

cur_classifiers = [
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Operating System :: POSIX",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: MIT License",
]

install_requires = ["psutil"]

setuptools.setup(
    name="webtraffic",
    version="0.3.1",
    author="Abin Simon",
    author_email="abinsimon10@gmail.com",
    description="See web traffic info python",
    url="https://github.com/meain/traffic",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["traffic"],
    install_requires=install_requires,
    keywords=["speed", "web", "download", "upload"],
    classifiers=cur_classifiers,
    entry_points={"console_scripts": ["traffic = traffic.traffic:main"]},
)
