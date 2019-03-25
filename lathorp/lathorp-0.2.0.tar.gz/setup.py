import setuptools


with open('README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='lathorp',
    use_scm_version=True,
    description='pytest fixtures for PostgreSQL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eladkehat/lathorp',
    author='Elad Kehat',
    author_email='eladkehat@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database',
        'Topic :: Software Development :: Testing',
        'Typing :: Typed'
    ],
    keywords='pytest postgresql pgsql testing',
    packages=setuptools.find_packages(exclude=['tests', 'docs']),
    python_requires='>=3.7',
    install_requires=[
        'psycopg2-binary >= 2.7',
        'pytest >= 4.3',
        'testing.postgresql >= 1.3'
    ],
    setup_requires=['setuptools_scm']
)
