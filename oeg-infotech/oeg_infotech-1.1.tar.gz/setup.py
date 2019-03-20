import setuptools


long_description = """
# oeg.infotech.xml

Library for OrgEnergoGaz Infotech xml processing
"""

setuptools.setup(
    name = 'oeg_infotech',
    version = '1.1',
    author = 'Vitaly Bogomolov',
    author_email = 'mail@vitaly-bogomolov.ru',
    description = 'Library for OrgEnergoGaz Infotech xml processing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/vb64/oeg.infotech.xml',
    packages = ['oeg_infotech'],
    download_url = 'https://github.com/vb64/oeg.infotech.xml/archive/v1.1.tar.gz',
    keywords = ['python', 'OrgEnergoGaz', 'Infotech', 'xml'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
