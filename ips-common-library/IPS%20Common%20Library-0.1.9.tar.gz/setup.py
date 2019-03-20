

import setuptools

setuptools.setup(setup_requires=['pbr'], pbr=True)


# import setuptools
#
# #
# # To build: python3 setup.py sdist bdist_wheel
# # Push to PyPy: twine upload dist/*
# #
#
# with open("README.md", "r") as fh:
#     long_description = fh.read()
#
# setuptools.setup(
#     name="ips_common",
#     version="0.1.8",
#     author="The Office for National Statistics, U.K.",
#     author_email="author@example.com",
#     description="Common functions for the ONS IPS Project",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     packages=setuptools.find_packages(),
#     install_requires=['PyYAML==5.1'],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     package_data={
#         '': ['*.yaml']
#     }
# )