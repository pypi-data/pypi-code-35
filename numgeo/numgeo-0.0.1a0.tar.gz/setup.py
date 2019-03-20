import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="numgeo",
    version="0.0.1a0",
    url="https://github.com/eischaefer/numgeo",
    author="Ethan I. Schaefer",
    author_email="ethan.i.schaefer@gmail.com",
    license="GPL 3.0 or later",
    description="A geospatial package to support skeletonization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Note: Version requirements reflect earliest tested version. It is
    # possible that earlier versions would also work.
    # Note: bottleneck and psutil are not strictly required for basic
    # functionality but are enforced here for performance and ease of
    # use, respectively. Limited functionality would be possible without
    # gdal.
    install_requires=["scipy>=0.19", "numpy>=1.13.3", "bottleneck>=1.2.1",
                      "psutil>=3.3.0", "gdal>=2.1.3"],
    # Note: Version requirement reflects earliest tested version. It is
    # possible that earlier versions would also work.
    python_requires="~=2.7.3",
    scripts=["./numgeo/scripts/skel/SkeletonScript.py"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: GIS",
    ],

    )
