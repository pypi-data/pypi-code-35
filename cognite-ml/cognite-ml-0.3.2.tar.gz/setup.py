import re

from setuptools import find_packages, setup
from distutils.extension import Extension
from setuptools.command.build_ext import build_ext

packages = find_packages(exclude=["tests*"])

version = re.search('^__version__\s*=\s*"(.*)"', open("cognite_ml/__init__.py").read(), re.M).group(1)

ext_modules = [
    Extension(
        "cognite_ml.filters.perona_malik",
        ["cognite_ml/filters/perona_malik.pyx"],
        cython_directives={"c_string_type": "str", "c_string_encoding": "utf8"},
        language="c++",
    ),
    Extension(
        "cognite_ml.timeseries.pattern_search.algorithms.DTW.pydtw",
        ["cognite_ml/timeseries/pattern_search/algorithms/DTW/pydtw.pyx"],
    ),
]

# Avoid toplevel Cython and numpy imports so that pip install works.
class DelayedBuildExt(build_ext):
    def run(self):
        import numpy

        self.include_dirs.append(numpy.get_include())
        super().run()

    def finalize_options(self):
        from Cython.Build import cythonize

        self.distribution.ext_modules[:] = cythonize(self.distribution.ext_modules)
        super().finalize_options()


setup(
    name="cognite-ml",
    version=version,
    description="Cognite Machine Learning Toolkit",
    url="https://github.com/cognitedata/cognite_ml",
    download_url="https://github.com/cognitedata/cognite_ml/archive/{}.tar.gz".format(version),
    author="Data Science Cognite",
    author_email="que.tran@cognite.com",
    packages=packages,
    install_requires=["cognite-sdk>=0.12", "numpy", "pandas", "scikit-learn", "tslearn"],
    setup_requires=["cython", "numpy"],
    include_package_data=True,
    ext_modules=ext_modules,
    cmdclass={"build_ext": DelayedBuildExt},
)
