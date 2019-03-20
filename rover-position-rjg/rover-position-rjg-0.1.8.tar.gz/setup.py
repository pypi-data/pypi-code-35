import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Check for '__main__' stops tests complaining about freeze_support()
if __name__ == '__main__':
    setuptools.setup(
        name="rover-position-rjg",
        version="0.1.8",
        author="Richard Gemmell",
        author_email="16683467+Richard-Gemmell@users.noreply.github.com",
        description="A python module to provide the heading and position for a small robot.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Richard-Gemmell/rover-position-rjg",
        license="LICENSE.txt",
        packages=setuptools.find_packages(),
        package_data={
            'rover_position_rjg': ['*.json']
        },
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Embedded Systems",
        ],
        install_requires=[
            "smbus2 >= 0.2",
            "spidev >= 3.2",
            "callee >= 0.3",
            "jsonpickle >= 1.0",
            "nose >= 1.3.7",
            "numpy >= 1.15.0",
            "paho-mqtt >= 1.4.0",
            "RPi.GPIO >= 0.6.4",
            "scipy >= 1.2.0",
            "testfixtures >= 6.3.0",
            "lsm9ds1-rjg >= 0.9",
            "decawave-1001-rjg >= 1.0"
        ]
    )