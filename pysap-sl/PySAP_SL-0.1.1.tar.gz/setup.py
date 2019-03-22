import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
      name="PySAP_SL",
      version="0.1.1",
      description="Automation tool for source list in SAP",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/y4ss/PySAP_SL",
      author="Yacine BEKKA",
      author_email="yacinebekka@yahoo.fr",
      license="MIT",
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Development Status :: 3 - Alpha",
          "Operating System :: Microsoft :: Windows",
      ],
      packages=find_packages(exclude=("test",)),
      include_package_data=True,
)
