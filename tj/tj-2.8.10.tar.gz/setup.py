from setuptools import setup
import tj

setup(
    name="tj",
    version=tj.__version__,
    description="A simple but powerful module that will provide you many useful methods.",
    long_description="A simple but powerful module that will provide you many useful methods.",
    author="Tushar Jain",
    author_email="tusharlock10@gmail.com",
    py_modules=['tj'],
    install_requires=[
        'autopy',
        'pyAesCrypt',
        'cryptography',
        'forex-python',
        'colorama']
)
