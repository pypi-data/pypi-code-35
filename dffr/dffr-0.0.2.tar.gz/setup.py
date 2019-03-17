import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dffr',
    version='0.0.2',
    author='Vladyslav Krylasov',
    author_email='vladyslav.krylasov@gmail.com',
    description='Find a difference between two mutable Python types.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vald-phoenix/dffr',
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
