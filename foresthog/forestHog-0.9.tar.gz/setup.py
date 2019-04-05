from setuptools import setup, find_packages

setup(
    name='forestHog',
    version='0.9',
    description='Searches through git repositories for high entropy strings, digging deep into commit history.',
    url='https://github.com/EbryxLabs/forestHog',
    author='Rana Awais',
    author_email='rana.awais@ebryx.com',
    license='GNU',
    packages = ['forestHog'],
    install_requires=[
        'GitPython == 2.1.1',
        'truffleHogRegexes == 0.0.7'
    ],
    entry_points = {
      'console_scripts': ['foresthog = forestHog.forestHog:main'],
    },
)
