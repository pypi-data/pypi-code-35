import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygments-lexer-overrides",
    version="0.0.1",
    author="Brightspot",
    author_email="mlautman@brightspot.com",
    description="Provides improved Pygments lexers",
    long_description=long_description,
    url="https://github.com/markperfectsensedigital/custom_lexers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

