import re
from setuptools import setup, find_packages

with open('skykit/__init__.py', encoding='utf-8') as f:
    version = re.search(r"__version__\s*=\s*'(\S+)'", f.read()).group(1)

with open("README.md", "r") as f:
    long_description = f.read()

test_deps = [
    'coverage',
    'pytest',
    'pytest-mock'
]

setup(
    name="skykit",
    version=version,
    author="Hassen Taidirt",
    author_email="htaidirt@gmail.com",
    description="Out-of-the-box methods for satellite imagery processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/htaidirt/skykit",
    packages=find_packages(),
    install_requires=[
        "sentinelsat",
    ],
    tests_require=test_deps,
    extras_require={
        'test': test_deps,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
