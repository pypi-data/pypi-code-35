#
# # Set the version tag: git tag -a 0.1.9 -m "version 0.1.9"
# # To build: python3 setup.py sdist bdist_wheel
# # Push to PyPy: twine upload dist/*
# #
#
# with open("README.md", "r") as fh:
#     long_description = fh.read()
#


import setuptools

setuptools.setup(setup_requires=['pbr'], pbr=True)

