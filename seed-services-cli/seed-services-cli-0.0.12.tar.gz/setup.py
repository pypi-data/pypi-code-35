from setuptools import setup, find_packages

setup(
    name="seed-services-cli",
    version="0.0.12",
    url='http://github.com/praekelt/seed-services-cli',
    license='BSD',
    description="A command-line interface for Seed Services HTTP APIs",
    long_description=open('README.rst', 'r').read(),
    author='Praekelt Foundation and Individual Contributors',
    author_email='support@praekeltfoundation.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'click-config',
        'seed-services-client==0.37.0',
        'demands==3.0.0',
    ],
    entry_points="""
        [console_scripts]
        seed-services-cli=seed_services_cli.main:cli
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
