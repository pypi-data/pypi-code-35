from setuptools import setup, find_packages
setup(
    name = 'DSwhois',
    version = '0.0.1',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'DSwhois = DSwhois.__main__:main'
        ]
    })
