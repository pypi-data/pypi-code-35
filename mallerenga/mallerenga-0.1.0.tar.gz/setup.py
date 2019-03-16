import pathlib
from setuptools import find_packages, setup

PROJECT_DIR = pathlib.Path(__file__).parent

README = (PROJECT_DIR / 'README.md').read_text()

setup(
    name='mallerenga',
    version='0.1.0',
    description='Handle Twitter accounts',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/pybcn/mallerenga',
    author='Ignasi Fosch',
    author_email='natx@y10k.ws',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=('tests', )),
    include_package_data=True,
    install_requires=['tweepy', 'click', ],
)
