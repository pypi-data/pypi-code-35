# Use pip install to download the last version of Elm and Elm format
# and install it in the path.
import atexit
import codecs
import os
import platform
import sys
from setuptools import setup
from setuptools.command.install import install
from urllib.request import urlopen
from io import BytesIO
import tarfile
import zipfile

HERE = os.path.abspath(os.path.dirname(__file__))


class CustomInstall(install):
    def run(self):
        def _post_install(self):
            def wrapper():
                version_parts = self.config_vars["dist_version"].split(".")
                version = ".".join(version_parts[:3])

                def find_module_path():
                    for p in sys.path:
                        if os.path.isdir(p) and "lib/python" in p:
                            env, _ = p.split("lib/python")
                            return os.path.join(env, "bin")

                install_path = find_module_path()

                # Find the OS
                system = platform.system()

                # Find the related archive in Github
                if system == "Linux":
                    url = f"https://github.com/avh4/elm-format/releases/download/{version}/elm-format-{version}-linux-x64.tgz"
                elif system == "Darwin":
                    url = f"https://github.com/avh4/elm-format/releases/download/{version}/elm-format-{version}-mac-x64.tgz"
                elif system == "Windows":
                    url = f"https://github.com/avh4/elm-format/releases/download/{version}/elm-format-{version}-win-i386.zip"

                print(f"Downloading {url}")
                # Download the archive
                with urlopen(url) as response:
                    archive = BytesIO(response.read())

                # Extract the archive
                if system == "Windows":
                    with zipfile.ZipFile(archive, "r") as zip_ref:
                        print(f"Extracting in {install_path}")
                        zip_ref.extractall(install_path)
                else:
                    tar = tarfile.open(fileobj=archive)
                    print(f"Extracting in {install_path}")
                    tar.extractall(path=install_path)
                    tar.close()

            return wrapper

        atexit.register(_post_install(self))
        install.run(self)


with codecs.open(os.path.join(HERE, "README.rst"), encoding="utf-8") as f:
    README = f.read()


with codecs.open(os.path.join(HERE, "CHANGELOG.rst"), encoding="utf-8") as f:
    CHANGELOG = f.read()


with codecs.open(os.path.join(HERE, "CONTRIBUTORS.rst"), encoding="utf-8") as f:
    CONTRIBUTORS = f.read()


setup(
    name="elm-format",
    version="0.8.1.1",
    description="elm-format installer",
    long_description=README + "\n\n" + CHANGELOG + "\n\n" + CONTRIBUTORS,
    license="Apache License (2.0)",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="web services",
    author="Rémy Hubscher",
    author_email="remy@chefclub.tv",
    url="https://github.com/natim/elm-format-installer",
    packages="",
    include_package_data=False,
    zip_safe=False,
    cmdclass={"install": CustomInstall},
)
