import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
REQUIREMENTS = (HERE / "requirements.txt").read_text()

setup(
    name="Lupv",
    version="1.6.36",
    description="Lup viewer",
    long_description=README,
    long_description_content_type="text/markdown",
    author="azzamsa",
    author_email="azzam@azzamsa.com",
    url="https://gitlab.com/azzamsa/lupv",
    packages=find_packages(),
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=REQUIREMENTS,
    entry_points={"gui_scripts": ("lupv = Lupv.main:main")},
)
