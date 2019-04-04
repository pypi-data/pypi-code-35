from setuptools import setup
setup(
    name='psycopg2-logical-decoding-json-consumer',
    version='1.1',

    description="PostgreSQL logical replication consumer library for the logical-decoding-json logical decoding output plugin",
    url="https://bitbucket.org/gclinch/psycopg2-logical-decoding-json-consumer",
    license='Apache License, Version 2.0',

    author='Graham Clinch',
    author_email='g.clinch@lancaster.ac.uk',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database'
    ],

    packages=['psycopg2_logical_decoding_json_consumer'],
    install_requires=['psycopg2'],
)
