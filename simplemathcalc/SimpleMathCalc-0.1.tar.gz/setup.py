# coding=utf8
import SimpleMathCalc

__author__ = 'LZU_Group_5'

from setuptools import setup
from setuptools import find_packages

setup(
    name="SimpleMathCalc",
    version=0.1,
    author="LZU_Group_5",
    author_email="blli18@lzu.edu.cn",
    url="https://github.com/BingliangLI/SimpleMathCalc",
    description="This is calculator that can calculate arithmometer, average number, median number, mode number, "
                "hex conversion, square and so on. Don't except you will be cool using this calc, it is like a "
                "poetaster! But anyway I learned how to share this project on Github and tried to publish it to PyPI",
    keywords="calculator",
    license="GNU General Public License v3.0",
    packages=find_packages(),
    install_requires=[]
)