import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


with open('requirements.txt', 'r') as f:
    requirements = f.readlines()


setuptools.setup(
    name='miceless',
    version='1.0.0',
    maintainer='Dmytro Tkanov',
    maintainer_email='akademi4eg@gmail.com',
    license='Apache License 2.0',
    description='Hotkeys for mouse click events.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/akademi4eg/miceless',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: POSIX :: Linux",
            "Environment :: X11 Applications",
            "Intended Audience :: End Users/Desktop",
            "Topic :: Utilities",
        ],
)
