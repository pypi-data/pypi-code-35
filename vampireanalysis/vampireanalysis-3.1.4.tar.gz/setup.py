import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vampireanalysis",
    version="3.1.4",
    author="Kyu Sang Han",
    author_email="khan21@jhu.edu",
    description="Vampire Image Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wirtzlab.johnshopkins.edu",
    packages=setuptools.find_packages(),
    install_requires=[
        'scipy==1.2.1',
        'pandas==0.24.1', 
        'numpy==1.16.2', 
        'pillow==5.4.1',
        'matplotlib==2.2.4', 
        'scikit-learn==0.20.3', 
        'scikit-image==0.14.2',
        'opencv-python==4.0.0.21',
    ],
    scripts=['bin/vampire.py'],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ),
)