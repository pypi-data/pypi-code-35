from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="multiprocessing_wrap",
    version="0.0.1",
    description="Easier multiprocessing",
    author='Dominic Slee',
    author_email='domslee1@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        'multiprocess'
    ],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/domsleee/multiprocess',
    license='BSD'
)
