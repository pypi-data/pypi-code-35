from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version='0.1.2',
    name='noderegister',
    package='noderegister',
    description='A Simple tool that registers ec2 host information to a DynamoDB Table',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tony Vattathil',
    author_email='avattathil@gmail.com',
    url='https://avattathil.github.io/node_register',
    license='Apache License 2.0',
    download_url='https://github.com/avattathil/noderegister/tarball/master',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Operating System :: POSIX :: Linux',
    ],
    scripts=[
        'bin/noderegister'
    ],
    keywords=['aws', 'noderegister'],
    install_requires=required,
#    test_suite="tests",
#    tests_require=["mock", "boto3"],
    include_package_data=True
)
