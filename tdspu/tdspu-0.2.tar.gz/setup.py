from setuptools import setup, find_packages

setup(
    name="tdspu", # THREDDS Data Server Publication Utils
    version="0.2",
    packages=find_packages(),
    package_data={
        'src': ['data/*.j2'],
    },

    author="zequihg50",
    author_email="ezequiel.cimadevilla@unican.es",
    description="Utils for NcML and TDS catalog generation",
)
