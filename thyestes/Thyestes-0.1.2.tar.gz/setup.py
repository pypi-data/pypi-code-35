from setuptools import setup, find_packages
import os
import thyestes
import thyestes.timerservice


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
thyestes.timerservice.Timerservice.dump_schema(extract_path("config_schema.json"))

setup(
    name='Thyestes',
    version=thyestes.version,
    packages=find_packages(),
    license='MIT license',
    long_description=read('README.rst'),
    description="Thyestes it a timer microservice. Listens on topics for specific messages, starts a timer when such "
                "a messages has been received and publishes a predefined message after the timer expired.",
    url='https://gitlab.com/pelops/skeiron/',
    author='Tobias Gawron-Deutsch',
    author_email='tobias@strix.at',
    keywords='mqtt forward echo ping service',
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
        "pelops>=0.4.0",
    ],
    test_suite="tests_unit",
    entry_points={
        'console_scripts': [
            'thyestes = thyestes.timerservice:standalone',
        ]
    },

)
