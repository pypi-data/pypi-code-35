import sys

if sys.version_info < (3,3):
    sys.exit('Sorry, Python < 3.3 is not supported')

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='jupyter-openbis-extension',
    version= '0.1.0',
    author='Swen Vermeul |  ID SIS | ETH Zürich',
    author_email='swen@ethz.ch',
    description='Extension for Jupyter notebooks to connect to openBIS and download/upload datasets, inluding the notebook itself',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://sissource.ethz.ch/sispub/jupyter-openbis-integration',
    packages=find_packages(),
    license='Apache Software License Version 2.0',
    install_requires=[
        'jupyter-nbextensions-configurator',
        'jupyter',
        'pybis>=1.8.4',
        'numpy',
    ],
    python_requires=">=3.3",
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("share/jupyter/nbextensions/jupyter-openbis-extension", [
            "jupyter-openbis-extension/static/main.js",
            "jupyter-openbis-extension/static/state.js",
            "jupyter-openbis-extension/static/common.js",
            "jupyter-openbis-extension/static/connectionDialog.js",
            "jupyter-openbis-extension/static/connections.js",
            "jupyter-openbis-extension/static/downloadDialog.js",
            "jupyter-openbis-extension/static/uploadDialog.js",
        ]),
        # like `jupyter nbextension enable --sys-prefix`
        ("etc/jupyter/nbconfig/notebook.d", [
            "jupyter-config/nbconfig/notebook.d/jupyter_openbis_extension.json"
        ]),
        # like `jupyter serverextension enable --sys-prefix`
        ("etc/jupyter/jupyter_notebook_config.d", [
            "jupyter-config/jupyter_notebook_config.d/jupyter_openbis_extension.json"
        ])
    ],
    zip_safe=False,
)
