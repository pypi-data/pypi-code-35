from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='forcelayout',
    version='1.0.6',
    description='Force-directed layout algorithms for Python',
    author='Iain Cattermole',
    author_email='iain_c@live.co.uk',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['forcelayout', 'forcelayout.algorithms'],
    install_requires=['numpy', 'matplotlib'],  # external packages as dependencies
)
