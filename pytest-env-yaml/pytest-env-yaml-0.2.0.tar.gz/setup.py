from setuptools import find_packages, setup

setup(
    name='pytest-env-yaml',
    version='0.2.0',
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'pytest11': [
            'env_yaml = pytest_env_yaml.plugin',
        ]
    },
    install_requires=[
        'pytest>=3.0.0',
        'PyYAML>=5.1,<6'
    ]
)
