from setuptools import setup, find_packages
import os
import hippasos
import hippasos.soundservice


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
hippasos.soundservice.SoundService.dump_schema(extract_path("config_schema.json"))

setup(
    name='Hippasos',
    version=hippasos.version,
    packages=find_packages(),
    license='MIT license',
    long_description=read('README.rst'),
    description='Hippasos plays preconfigured sound files upon reception of predefined mqtt messages.',
    url='https://gitlab.com/pelops/lysidike/',
    author='Tobias Gawron-Deutsch',
    author_email='tobias@strix.at',
    keywords='mqtt device driver rpi raspberry pi',
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
        "pygame",
    ],
    entry_points={
        'console_scripts': [
            'hippasos = hippasos.soundservice:standalone',
        ]
    },

)
