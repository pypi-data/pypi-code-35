from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read().strip()


def version():
    with open('VERSION') as f:
        return f.read().strip()


def requirements():
    with open('requirements.txt') as f:
        return f.read().strip().split('\n')


def classifiers():
    with open('classifiers.txt') as f:
        return f.read().strip().split('\n')


setup(
    name="scipolate",
    licence="GNU 3.0",
    version=version(),
    author="Mirko Maelicke",
    author_email="mirko.maelicke@kit.edu",
    description="helper for running different scipy 2D interpolations",
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=classifiers(),
    install_requirements=requirements(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)