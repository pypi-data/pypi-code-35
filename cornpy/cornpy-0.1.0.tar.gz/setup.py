import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'numpy>=1.7',
    'scipy>=0.14',
    'matplotlib>=1.3.1',
    'pandas>=0.13',
]

setuptools.setup(
    name="cornpy",
    version="0.1.0",
    author="Mauro Cavalcanti",
    author_email="maurobio@gmail.com",
    description="Cornell Ecology Programs in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maurobio/cornpy",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords=['ordination', 'classification', 'ecology', 'multivariate data analysis'],
    package_data={
        'cornpy': ['data/*.csv'],
    },
)