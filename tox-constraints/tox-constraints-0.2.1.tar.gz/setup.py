import setuptools

with open("requirements/install_requires.txt") as fp:
    install_requires = list(fp)

setuptools.setup(
    name="tox-constraints",
    version="0.2.1",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    entry_points={"tox": ["constraints = tox_constraints"]},
)
