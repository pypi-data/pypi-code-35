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

HERE = os.path.abspath(os.path.dirname(__file__))


class CustomInstall(install):
    def run(self):
        def _post_install(self):
            def wrapper():
                version_parts = self.config_vars["dist_version"].split(".")
                elm_version = ".".join(version_parts[:3])

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
                    url = f"https://github.com/elm/compiler/releases/download/{elm_version}/binaries-for-linux.tar.gz"
                elif system == "Darwin":
                    url = f"https://github.com/elm/compiler/releases/download/{elm_version}/binaries-for-mac.tar.gz"
                elif system == "Windows":
                    url = f"https://github.com/elm/compiler/releases/download/{elm_version}/binaries-for-windows.tar.gz"

                print(f"Downloading {url}")
                # Download the archive
                with urlopen(url) as response:
                    archive = BytesIO(response.read())

                # Extract the archive
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
    name="elm-lang",
    version="0.19.0.1",
    description="Elm compiler installer",
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
    url="https://github.com/natim/elm-lang",
    packages="",
    include_package_data=False,
    zip_safe=False,
    cmdclass={"install": CustomInstall},
)
