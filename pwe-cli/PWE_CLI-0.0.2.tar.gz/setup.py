import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split('\n')

setuptools.setup(
    name="PWE_CLI",
    version="0.0.2",
    author="Sahil Gupta",
    author_email="",
    description="A CLI Interface to the Possible Worlds Explorer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idaks/PWE-CLI",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['PWE_CLI/PWE_CLI_Scripts/pwe_run_clingo', 'PWE_CLI/PWE_CLI_Scripts/pwe_load_worlds',
             'PWE_CLI/PWE_CLI_Scripts/pwe_complexity_calc', 'PWE_CLI/PWE_CLI_Scripts/pwe_dist_calc',
             'PWE_CLI/PWE_CLI_Scripts/pwe_export', 'PWE_CLI/PWE_CLI_Scripts/pwe_query',
             'PWE_CLI/PWE_CLI_Scripts/pwe_visualize', 'PWE_CLI/PWE_CLI_Scripts/pwe_run_dlv',
             'PWE_CLI/PWE_CLI_Scripts/pwe-cli',
             ]
)