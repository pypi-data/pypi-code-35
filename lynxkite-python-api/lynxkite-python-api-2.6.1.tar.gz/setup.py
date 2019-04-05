import setuptools

setuptools.setup(
    name='lynxkite-python-api',
    version='2.6.1',
    author='Lynx Analytics',
    author_email='lynxkite@lynxanalytics.com',
    description='Python API for LynxKite',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://lynxkite.com/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
)
