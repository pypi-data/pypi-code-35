import setuptools
from setuptools.config import read_configuration

cfg_dict = read_configuration("setup.cfg")

try:
    print("checking for cython")
    # if cython is installed, use it to compile
    from Cython.Build import cythonize

    ext_mods = [setuptools.Extension("*",
            [
                "simpletree3/*.py"
            ])]
    setuptools.setup(
        test_suite="nose.collector",
        ext_modules=cythonize(ext_mods),
        **cfg_dict["metadata"]
    )

except ImportError:
    # no cython, fallback to pure python
    print("building pure python")
    setuptools.setup(
        test_suite="nose.collector",
        **cfg_dict["metadata"]
    )
