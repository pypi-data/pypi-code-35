# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

setup(
    name  = 'pumpernickel',
    version = '1.0.10',
    license = 'MIT',
    author = 'hiroyam',
    author_email = 'hogehoge@gmail.com',
    url = 'https://github.com/hiroyam/pumpernickel',
    packages = find_packages(),
    install_requires = [
        'ipython',
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'sklearn',
        ],
)
