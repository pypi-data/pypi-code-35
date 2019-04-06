from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='forestHog',
    version='1.2',
    description='Searches through git repositories for high entropy strings, '
                'digging deep into commit history.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EbryxLabs/forestHog',
    author='Rana Awais',
    author_email='rana.awais@ebryx.com',
    license='GNU',
    packages=['forestHog'],
    install_requires=[
        'GitPython == 2.1.1',
        'truffleHogRegexes == 0.0.7'
    ],
    entry_points={
        'console_scripts': [
          'foresthog = forestHog.forestHog:main',
          'git-forest = forestHog.gitForest:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent'
    ],
)
