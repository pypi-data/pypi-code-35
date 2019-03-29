from setuptools import setup, find_packages

install_requires = ['Pillow==5.4.1',
                    'pytest==4.3.1',
                    'SQLAlchemy==1.2.17',
                    'pyodbc==4.0.26']

setup(
    name='podder-lib',
    version='0.0.3',
    description='Library for the Podder Task.',
    packages=find_packages(),
    author="podder-ai",
    url='https://github.com/podder-ai/podder-lib',
    include_package_data=True,
    install_requires=install_requires
)
