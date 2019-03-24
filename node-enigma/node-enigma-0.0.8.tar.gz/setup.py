from setuptools import setup , find_packages

setup(
    name='node-enigma',
    version='0.0.8',
    url="https://github.com/dyeboah/enigma.py",
    author="David Yeboah",
    author_email="dyeboah@oswego.edu",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Argparse', 'Requests', 
    ],
    entry_points='''
        [console_scripts]
        enigma=scripts.enigma:main
    ''',
    license=['MIT'],
    keyword= "enigma machine node",
)