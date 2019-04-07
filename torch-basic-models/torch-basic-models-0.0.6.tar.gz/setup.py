from setuptools import find_packages, setup

name = 'torch-basic-models'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.6',
    description='Basic Models for PyTorch, with Unified Interface',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='PyTorch Basic Models',
    packages=find_packages(exclude=['tests', f'{module}.configs.build']),
    package_data={f'{module}': ['schema/*.json']},
    entry_points={'sf.torch.model': f'Basic = {module}'},
    install_requires=[
        'jsonschema',
        'json-schema-to-class>=0.0.8',
        'mobile-block',
        'torch',
        'torch-model-loader>=0.0.3'
    ]
)
