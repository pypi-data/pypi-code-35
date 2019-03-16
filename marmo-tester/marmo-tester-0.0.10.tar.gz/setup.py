from setuptools import find_packages, setup


setup(
    name='marmo-tester',
    
    version="0.0.10",
    
    description='Marmo wallet Python SDK',
    
    author='Agustin Aguilar',
    
    author_email='agusxrun@gmail.com',
    py_modules=["marmotester"],
    url='',

    entry_points={
        'console_scripts': [
            'marmo-tester=marmotester:main',
        ],
    },

    install_requires=[
        "marmopy==0.4.0"
    ],

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],    
)
