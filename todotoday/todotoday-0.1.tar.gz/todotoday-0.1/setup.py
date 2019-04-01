import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="todotoday",
    version="0.1",
    author="Joshua Kurtenbach",
    author_email="38633896+BelatedMussel@users.noreply.github.com",
    description="A simple to-do list program.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/BelatedMussel/todotoday",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
