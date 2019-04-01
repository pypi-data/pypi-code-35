import setuptools


with open('mhtg-requirements.txt') as f:
    install_requires = list(f)


setuptools.setup(
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    install_requires=install_requires,
)
