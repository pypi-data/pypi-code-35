import setuptools

setuptools.setup(
    name="pipomatic",
    version="4.2",
    author="eq8r",
    author_email="doug.hudgeon@eq8r.com",
    description="Automating the creation of an installable PIP module from a Jupyter notebook",
    long_description="One of the challenges with writing code in a Jupyter notebook is that it is hard to re-use functions. Pipomatic allows you to create pip-installable modules from the functions in your Jupyter notebook.",
    long_description_content_type="text/markdown",
    url="https://github.com/eq8r/pipomatic",
    py_modules = ["pipomatic"],
    install_requires=[
        'black',
        'click',
        'ipython',
        'nbformat',
        'nbconvert',
        'setuptools',
        'twine',
        'wheel'
    ],
    entry_points={
        'console_scripts': [
            'pipomatic=pipomatic:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)