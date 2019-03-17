from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

# Import the project version
with open("bdf2ttf/__version__.py", "r") as version_file:
    exec(version_file.read())

setup(
        name="bdf2ttf",
        version=__version__,
        description="Convert bitmap fonts into TTF format",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Gabriel Holodak",
        author_email="gabriel.holodak@gmail.com",
        url="https://github.com/keidax/bdf2ttf.py",
        packages=find_packages(),
        install_requires=["bdflib", "pyyaml"],
        python_requires='>=3',
        entry_points={
            "console_scripts": [
                "bdf2ttf=bdf2ttf.convert:main",
                "yml2fea=bdf2ttf.feature:main"
                ]
            },
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            ]
        )
