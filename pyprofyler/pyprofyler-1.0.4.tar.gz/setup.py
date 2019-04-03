from os.path import exists
from setuptools import setup
setup(
	name='pyprofyler',
	version='1.0.4',
	author='Aly Shmahell',
	author_email='aly.shmahell@gmail.com',
	url='https://github.com/AlyShmahell/PyProfyler',
	description='a simple memory profiler for python programs.',
	long_description=(open('README.md', encoding='utf-8').read() if exists('README.md')
                        else ''),
    long_description_content_type='text/markdown',
	packages=['pyprofyler'],
	install_requires=[
			  "psutil==5.6.1",
			  "cython==0.29.6",
			  "numpy==1.16.2"
			],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)