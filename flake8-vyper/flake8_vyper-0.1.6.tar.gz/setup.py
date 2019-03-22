import setuptools

requires = [
    "flake8>=3.0.0",
    "vyper==0.1.0b9"
]

long_description = ''
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flake8_vyper",
    license="MIT",
    version="0.1.6",
    description="Plugin for flake8 to support Vyper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mike Shultz",
    author_email="mike@mikeshultz.com",
    url="https://gitlab.com/mikeshultz/flake8-vyper",
    py_modules=['vyper_cli'],
    install_requires=requires,
    entry_points={
        "console_scripts": [
            'flake8-vyper = vyper_cli:main',
        ]
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
