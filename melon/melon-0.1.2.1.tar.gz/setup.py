import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="melon",
    version="0.1.2.1",
    author="romanjoffee",
    author_email="roman.jugai@gmail.com",
    description="Lightweight package meant to simplify data processing for Deep Learning",
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    packages=setuptools.find_packages(),
    url="https://github.com/romanjoffee/melon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click==7.0", "tqdm==4.29.0", "tqdm==4.29.0", "pillow==5.4.1"],
    entry_points={
        "console_scripts": [
            "melon=scripts.cli:cli"
        ]
    }
)
