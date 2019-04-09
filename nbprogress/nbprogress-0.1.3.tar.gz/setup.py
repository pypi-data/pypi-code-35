import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: MIT License',
    'Topic :: Utilities']

setuptools.setup(
    name="nbprogress",
    version="0.1.3",
    python_requires='>=3.*',
    author="saberd",
    author_email="mail@saberd.com",
    description="A lightweigth progressbar for jupyter notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saberd/nbprogress",
    packages=setuptools.find_packages(),
    py_modules=['nbprogress'],
    install_requires=[
        'ipywidgets',
        'IPython',
    ],
    classifiers=classifiers,
)