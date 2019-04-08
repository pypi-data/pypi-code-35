from setuptools import setup, find_packages

setup(
    name='merpy',
    version='0.0.1',
    description='use MER inside python',
    author='Andre Lamurias',
    author_email='alamurias@lasige.di.fc.ul.pt',
    packages=["merpy-dev"],
    keywords=['ner', 'mer'],
    url='https://github.com/lasigeBioTM/merpy',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)