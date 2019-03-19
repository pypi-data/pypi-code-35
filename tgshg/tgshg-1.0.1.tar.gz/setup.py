import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tgshg",
    version="1.0.1",
    author="tgshg",
    author_email="tgshgworld@gmail.com",
    description="A test small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tgshg/pypi/tgshg",
    packages=setuptools.find_packages(),
    classifiers=[
        # https://pypi.org/classifiers/
        # "Development Status ::1 - Planning",
        "Environment :: Plugins",
        # "Framework :: IDLE",
        "Intended Audience :: Developers",
        # "License :: OSI Approved :: MIT License",
        "License :: Free for non-commercial use",
        "Natural Language :: Chinese (Simplified)",
        # "Natural Language :: English",
        # "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 2",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)