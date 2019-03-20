__requires__ = "Lupr"
import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
REQUIREMENTS = (HERE / "requirements.txt").read_text()

setup(
    name="Lupr",
    version="1.5.4",
    description="Lup recorder",
    long_description=README,
    long_description_content_type="text/markdown",
    author="azzamsa",
    author_email="azzam@azzamsa.com",
    url="https://gitlab.com/azzamsa/lupr",
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
    entry_points={"gui_scripts": ("lupr = Lupr.main:main")},
)
