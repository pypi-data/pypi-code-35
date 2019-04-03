from setuptools import setup

setup(
    name='mly',
    version='0.0.1',
    author='Vasileios Skliris',
    author_email='vas.skliris@gmail.com',
    url='http://pypi.python.org/pypi/mly/',
    license='LICENSE.txt',
    description='Dataset generation and tools for ML in gravitational waves',
    long_description=open('README.txt').read(),
    install_requires=[
        "gwpy >= 0.13.1",
        "Keras >= 2.2.4",
        "tensorflow >= 1.12.0",
        "numpy >= 1.16.1"
    ]
)