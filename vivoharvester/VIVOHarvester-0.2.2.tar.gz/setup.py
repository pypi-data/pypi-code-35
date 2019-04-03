import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VIVOHarvester",
    version="0.2.2",
    author="Yinlin Chen, Tingting Jiang, Lee Hunter",
    author_email="ylchen@vt.edu, virjtt03@vt.edu, whunter@vt.edu",
    description="VIVO harvester",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VTUL/VIVOHarvester",
    scripts=['bin/vivotool'],
    packages=setuptools.find_packages(),
    install_requires=[
        'nose',
        'rdflib',
        'xmltodict',
        'pyyaml',
        'lxml',
        'requests',
        'cryptography',
        'pytz',
        'pymysql'
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
