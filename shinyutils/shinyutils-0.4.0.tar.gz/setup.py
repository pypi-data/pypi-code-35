import os
from setuptools import setup

readme_file = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_file) as f:
    long_description = f.read()

setup(
    name="shinyutils",
    version="0.4.0",
    description="Various utilities for common tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jayanthkoushik/shinyutils",
    author="Jayanth Koushik",
    author_email="jnkoushik@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    packages=["shinyutils"],
    package_data={"shinyutils": ["data/mplcfg.json"]},
    install_requires=["matplotlib", "seaborn", "crayons"],
    python_requires=">=3.4",
    extras_require={
        "dev": ["black", "pylint", "isort", "twine", "wheel", "bumpversion"]
    },
)
