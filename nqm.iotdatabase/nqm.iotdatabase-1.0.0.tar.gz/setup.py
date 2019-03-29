from setuptools import setup

# required for gets the current version of the package
import nqm.iotdatabase

setup(
    name='nqm.iotdatabase',
    version=nqm.iotdatabase.__version__,
    packages=['nqm.iotdatabase', 'nqm.iotdatabase.ndarray'],
    author='Alois Klink',
    author_email='alois.klink@gmail.com',
    description="Library for accessing a local nqm-iot-database",
    include_package_data=False, # don't include documentation
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/nqminds/nqm-iot-database-py/issues",
        "Documentation": "https://nqminds.github.io/nqm-iot-database-py/",
        "Source Code": "https://github.com/nqminds/nqm-iot-database-py",
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nqminds/nqm-iot-database-py',
    install_requires=['sqlalchemy', 'mongosql>=1.5.1-0', 'shortuuid', 'numpy', 'future'],
    zip_safe=True,
)
