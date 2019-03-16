from setuptools import setup, find_packages
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyepgnotify",
    version="0.1.2",
    license="GPLv3",
    url="https://github.com/Aikhjarto/pyepgnotify.git",
    download_url="https://github.com/Aikhjarto/pyepgnotify/archive/v0.1.1.tar.gz",
    keywords=["VDR", "EPG", "mail", "notification"],
    author="Thomas Wagner",
    author_email="wagner-thomas@gmx.at",
    description="Reads EPG data from VDR and sends user notification mails when desired programs are found",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifies=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=["pyyaml"],
    entry_points={"console_scripts": ["pyepgnotify=pyepgnotify.epgnotify:main"]},
    data_files=[("pyepgnotify", ["epgnotify.yml"])],
)
