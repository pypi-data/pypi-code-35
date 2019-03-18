import setuptools

with open("README.md", "r") as ld:
    long_description = ld.read()

setuptools.setup(
    name="essay_scorer", 
    version="1.0",
    author="Matthew Martin",
    author_email="products@mkylemartin.com",
    description="An automated essay scorer for english language learner essays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkylemartin/essay_scorer",
    keywords=[
        'automated essay scorer',
        'essay',
        'gradient boosting regressor',
        'linguistics',
        'feature extraction'],
    packages=setuptools.find_packages(),
    install_requires=['progress'],
    python_requires='~=3.7',
    # scripts=['bin/essay_scorer'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
