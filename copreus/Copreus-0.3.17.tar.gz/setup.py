from setuptools import setup, find_packages
import os
import copreus.drivers
import copreus
import copreus.drivermanager.drivermanager

def get_console_scripts():
    scripts = [
        'copreus = copreus.drivermanager.drivermanager:standalone',
        'copreus_drivermanager = copreus.drivermanager.drivermanager:standalone',
    ]

    drivers = copreus.drivers.get_drivers()
    for k, driver in drivers.items():
        script_name = "copreus_" + (driver["name"]).lower()
        script = driver["module"] + ":standalone"
        scripts.append(script_name + " = " + script)

    return scripts


def extract_path(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read(fname):
    return open(extract_path(fname)).read()


# convert README.md into README.rst - *.md is needed for gitlab; *.rst is needed for pypi
if os.path.isfile(extract_path('README.md')):
    try:
        from pypandoc import convert
        readme_rst = convert(extract_path('README.md'), 'rst')
        with open(extract_path('README.rst'), 'w') as out:
            out.write(readme_rst + '\n')
    except ModuleNotFoundError as e:
        print("Module pypandoc could not be imported - cannot update/generate README.rst.", e)


# update config schema json.
copreus.drivermanager.drivermanager.DriverManager.dump_schema(extract_path("config_schema.json"))

setup(
    name='Copreus',
    version=copreus.version,
    packages=find_packages(),
    license='MIT license',
    long_description=read('README.rst'),
    description='This library provides a framework to write device drivers for the raspberry pi that are connected to MQTT.',
    url='https://gitlab.com/pelops/copreus/',
    author='Tobias Gawron-Deutsch',
    author_email='tobias@strix.at',
    keywords='mqtt device driver rpi raspberry pi',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.5',
    install_requires=[
        "RPi.GPIO",
        "pelops>=0.3.5",
    ],
#    dependency_links=[
#        adc - spidev
#        bme280 - smbus2, bme280
#        dac - spidev
#        dht - Adafruit_DHT
#        epaper - spidev, Pillow (...)
#        input - nix
#        output - nix
#        rotaryencoder - nix
#    ],
    test_suite="tests_unit",
    entry_points={
        'console_scripts': get_console_scripts()
    },

)
