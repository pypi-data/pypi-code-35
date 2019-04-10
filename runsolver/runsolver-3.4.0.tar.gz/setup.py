import os
import sys
import subprocess

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py


class Build(build_py):
    def run(self):
        make_runsolver = ["make", "runsolver"]
        runsolver_dir = os.path.join(
            os.path.dirname(__file__), "runsolver", "runsolver"
        )
        if subprocess.call(make_runsolver, cwd=runsolver_dir) != 0:
            sys.exit(-1)
        build_py.run(self)


setup(
    name="runsolver",
    version="3.4.0",
    packages=find_packages(),
    cmdclass={"build_py": Build},
    entry_points={"console_scripts": ["runsolver=runsolver:run"]},
    package_data={"runsolver": ["runsolver/*"]},
)
