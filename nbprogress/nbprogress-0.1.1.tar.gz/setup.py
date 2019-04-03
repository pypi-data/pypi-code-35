import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbprogress",
    version="0.1.1",
    python_requires='>=3.*',
    author="saberd",
    author_email="mail@saberd.com",
    description="A lightweigth progressbar for jupyter notebook",
    long_description="Important to enable enable ipythonwidgets by running \
        ```Python \
        jupyter nbextension enable --py widgetsnbextension \
        ```",
    long_description_content_type="text/markdown",
    url="https://github.com/saberd/nbprogress",
    packages=setuptools.find_packages(),
    py_modules=['nbprogress'],
    install_requires=[
        'ipywidgets',
        'IPython',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)