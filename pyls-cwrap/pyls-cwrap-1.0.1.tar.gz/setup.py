import os
from typing import Any, Dict

from setuptools import find_packages, setup

about: Dict[str, Any] = {}

with open(os.path.join(os.path.dirname(__file__), "pyls_cwrap", "__about__.py")) as f:
    exec(f.read(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],
    license=about["__license__"],
    platforms="Any",
    packages=find_packages(),
    provides=["pyls_cwrap"],
    install_requires=["python-language-server", "pheasant"],
    entry_points={"pyls": ["pyls_cwrap = pyls_cwrap.plugin"]},
)
