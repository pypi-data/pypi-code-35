import pathlib
import setuptools

setuptools.setup(
    name="qmp",
    version="0.0.1",
    description="QEMU Monitor Protocol client",
    url="https://gitlab.com/abogdanenko/qmp",
    py_modules=["qmp"],
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    maintainer="Alexey Bogdanenko",
    maintainer_email="alexey@bogdanenko.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
)
