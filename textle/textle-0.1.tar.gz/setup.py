from setuptools import setup, find_packages

with open("requirements.txt") as f:
    reqs = f.read().splitlines()

setup(
    name="textle",
    version="0.1",
    packages=find_packages(),
    install_requires = reqs,
    entry_points = {
        'console_scripts': ['textle=textle.cli.cli:textle']
    },

    description="A build tool to assist in managing document creation pipelines.",
    author="Matthew Mirvish",
    author_email="matthew@mm12.xyz",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
        'Environment :: Console'
    ],

    keywords="latex pandoc automation tool cli click pipeline",
    url="https://github.com/mincrmatt12/textle",
    project_urls={
        "Bug Tracker": "https://github.com/mincrmatt12/textle/issues",
        "Source Code": "https://github.com/mincrmatt12/textle",
        "Documentation": "https://textle.readthedocs.io"
    }
)
