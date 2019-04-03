from setuptools import find_packages, setup

name = 'torch-lr-scheduler'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.1',
    description='PyTorch Optimizer Lr Scheduler',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='PyTorch Lr Scheduler',
    packages=find_packages(exclude=['tests', f'{module}.configs.build']),
    package_data={f'{module}': ['schema/*.json']},
    install_requires=[
        'jsonschema',
        'json-schema-to-class>=0.1.0',
        'torch',
    ]
)
