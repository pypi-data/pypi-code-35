import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='chronos-cli',
    version='0.2.9',
    author='Claude Léveillé',
    author_email='claude-leveille@outlook.com',
    description='A CLI tool that infers a next version number for Git repos.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devoperate/chronos',
    packages=setuptools.find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'chronos=chronos.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
