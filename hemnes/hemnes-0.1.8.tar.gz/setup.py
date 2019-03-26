import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemnes",
    version="0.1.8",
    author="Sayeef Moyen",
    author_email="develop.sayeefrm@gmail.com",
    description="An in-depth ikea scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sayeefrmoyen/hemnes",
    packages=setuptools.find_packages(exclude=['data', 'docs']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='scraping ikea ikea-scraping python3 beautifulsoup, beautiful-soup',
    install_requires=['selenium', 'bs4'],
    python_requires='>=3',
)
