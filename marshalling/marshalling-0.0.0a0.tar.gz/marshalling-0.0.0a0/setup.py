import setuptools


setuptools.setup(
    name="marshalling",
    version="0.0.0.a",
    author="Praveen Baburao Kulkarni",
    author_email="praveenneuron@gmail.com",
    description="A library to add marshalling support for dataclasses "
                "introduced from Python 3.6+",
    long_description="",
    long_description_content_type='text/x-rst',
    url="https://github.com/SpikingNeurons/marshalling.git",
    packages=setuptools.find_packages(),
    classifiers=[

        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    license="BSD 3",
)