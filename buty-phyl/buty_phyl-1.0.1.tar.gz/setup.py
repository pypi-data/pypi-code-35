from setuptools import setup

setup(
    name="buty_phyl",
    packages=['buty_phyl'],
    version="1.0.1",
    description="Inferring traits by 16S",
    author='Anni Zhang',
    author_email='anniz44@mit.edu',
    url='https://github.com/caozhichongchong/BayersTraits_16S',
    keywords=['16S', 'bacterial genomes', 'function', 'traits'],
    license='MIT',
    #install_requires=['python>=3.0'],
    include_package_data=True,
    long_description=open('README.md').read(),
    package_dir={'buty_phyl': 'buty_phyl'},
    package_data={'buty_phyl': ['scripts/*','data/*','example/*']},
    entry_points={'console_scripts': ['buty_phyl = buty_phyl.__main__:main']},
    #zip_safe=False,
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest'],
    classifiers=[
        #'Development Status :: 1 - Alpha',
        #'Intended Audience :: Bioinformatics and Researchers',
        #'License :: MIT',
        #'Operating System :: MacOS',
        #'Operating System :: Microsoft :: Windows',
        #'Operating System :: LINUX',
        'Programming Language :: Python :: 3',
        #'Topic :: Antibiotic resistance :: risk ranking',
        #'Topic :: Metagenomes :: Antibiotic resistance',
    ]
)
