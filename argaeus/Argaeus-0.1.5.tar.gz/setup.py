from setuptools import setup, find_packages
import os
import argaeus
import argaeus.thermostatguicontroller


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
argaeus.thermostatguicontroller.ThermostatGUIController.dump_schema(extract_path("config_schema.json"))

setup(
    name='Argaeus',
    version=argaeus.version,
    packages=find_packages(),
    license='MIT license',
    long_description=read('README.rst'),
    description='ThermostatGUIController (display and gui-logic) for a thermostat - to be used in combination with pelops/copreus and '
                'pelops/alcathous',
    url='https://gitlab.com/pelops/argaeus/',
    author='Tobias Gawron-Deutsch',
    author_email='tobias@strix.at',
    keywords='mqtt microservice thermostat controller',
    classifiers=[
        "Development Status :: 4 - Beta",
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
        "pelops>=0.3.8",
    ],
    test_suite="tests_unit",
    entry_points={
        'console_scripts': [
            'argaeus = argaeus.thermostatguicontroller:standalone',
        ]
    },

)
