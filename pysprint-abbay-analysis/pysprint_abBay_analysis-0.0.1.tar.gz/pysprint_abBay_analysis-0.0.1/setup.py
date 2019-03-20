from setuptools import setup, find_packages
with open("requirements.txt") as req_txt:
	required = [line for line in req_txt.read().splitlines() if line]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pysprint_abBay_analysis",
    version="0.0.1",
    author="Gender Minorities Py Sprints",
    author_email="author@example.com",
    description="Bayesian AB test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AngelaO/Bayesian-ABTest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_data=["requirements.txt"],
    install_requires=required,
    platforms=['any'],
    python_requires=">=3.3",
)
