import setuptools

setup = dict(
    name="ArduinoControllServer",
    version="0.1",
    author="Julian Kimmig",
    author_email="julian-kimmig@gmx.net",
    description="webframe for arduinocontroller",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JulianKimmig/arduino_controll_server",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
if __name__ == "__main__":
    setuptools.setup(**setup)
