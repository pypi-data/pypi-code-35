#! /usr/bin/env python
import os
import subprocess

from .contexts import cd
from .unix import is_linux, is_osx
from .url import download_url


def miniconda_url(version="latest", python="", url=None):
    if python not in ["", "2", "3"]:
        raise ValueError("Python version not understood")
    url = url or "http://repo.continuum.io/miniconda"

    if is_linux():
        os_name = "Linux-x86_64"
    elif is_osx():
        os_name = "MacOSX-x86_64"
    file = "Miniconda{python}-{version}-{os}.sh".format(
        python=python, version=version, os=os_name
    )

    return "/".join([url, file])


def download_miniconda(dest, cache="."):
    return download_url(miniconda_url(), dest, cache=cache)


def install_python(prefix=".", cache=None, packages=None):
    prefix = os.path.abspath(prefix)
    cache = cache or os.path.join(prefix, "var", "cache")
    packages = packages or []

    with cd(cache):
        miniconda = download_miniconda("miniconda.sh")

    with cd(prefix) as base:
        conda = os.path.join(base, "bin", "conda")

        if not os.path.exists(conda):
            subprocess.check_call(["bash", miniconda, "-f", "-b", "-p", base])

            subprocess.check_call(
                [
                    conda,
                    "config",
                    "--set",
                    "always_yes",
                    "yes",
                    "--set",
                    "changeps1",
                    "no",
                ]
            )
            subprocess.check_call([conda, "update", "conda"])

        for package in packages:
            subprocess.check_call([conda, "install", package])

    return prefix
