import setuptools

setuptools.setup(
    name='osrs_net',
    version='0.0.1',
    author='Patrick Seute',
    author_email='patrick.seute@gmail.com',
    description='Simple OSBuddy Exchange API Wrapper',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'requests'
    ]
)
