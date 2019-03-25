import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='dispyt',
    version='0.0.2b2',
    author='truedl',
    author_email='dauzduz1@example.com',
    description='📚 Dispyt is an API wrapper for the Discord API [Python3]',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/truedl/dispyt',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['asyncio', 'aiohttp', 'websockets'],
)