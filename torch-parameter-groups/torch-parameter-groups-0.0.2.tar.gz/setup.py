from setuptools import find_packages, setup

name = 'torch-parameter-groups'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.2',
    description='Group PyTorch Parameters according to Rules',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='PyTorch Parameter Groups',
    packages=find_packages(exclude=['tests', f'{module}.configs.build']),
    package_data={f'{module}': ['schema/*.json']},
    install_requires=[
        'jsonschema',
        'json-schema-to-class>=0.1.0',
        'torch',
    ]
)
