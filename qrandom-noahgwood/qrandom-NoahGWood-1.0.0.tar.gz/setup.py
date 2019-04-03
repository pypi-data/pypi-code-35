import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name='qrandom-NoahGWood',
    version='1.0.0',
    author="Noah Wood",
    author_email="ngwood111@gmail.com",
    description="Shrodingers Random Number Generator",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/NoahGWood/QRandom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
	],
    )
