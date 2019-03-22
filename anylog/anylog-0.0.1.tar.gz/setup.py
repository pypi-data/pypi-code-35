import setuptools

with open('README.rst', 'r') as file:
    long_description = file.read()
setuptools.setup(
    name='anylog',
    version='0.0.1',
    author='Oleksandr Popov',
    author_email='oleksandr.popov@outlook.com',
    description='Faster, small and easy logging framework',
    long_description=long_description,
    long_description_content_type=' text/x-rst',
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)