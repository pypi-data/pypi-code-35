import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name='Chronomancy',
    version='0.0.1',
    author='Jonathan Craig',
    author_email='blurr@iamtheblurr.com',
    description="The power of Time itself, for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=setuptools.find_packages(),
    url='https://github.com/IAmTheBlurr/Chronomancy',
    license='MIT',
)
