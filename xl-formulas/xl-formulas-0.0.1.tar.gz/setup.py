import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='xl-formulas',
    version='0.0.1',
    author='Joe Tatusko',
    author_email='tatuskojc@gmail.com',
    description='Helper to save Excel formulas from Pandas dataframes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/joetats/xlFormulas',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha'
        ''
    ],
)
