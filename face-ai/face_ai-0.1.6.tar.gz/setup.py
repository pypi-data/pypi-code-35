import setuptools
from frapi import __version__, __author__, __email__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'numpy',
    'Pillow',
    'grpcio',
    'tensorflow',
    'tensorflow-serving-api',
    'opencv-python'
]

setuptools.setup(
    name="face_ai",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Package for Face AI, including Face Detection & Face Recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ai.game.tw",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
