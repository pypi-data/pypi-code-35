from setuptools import setup,find_packages

setup(
    name="jget",
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    description="File downloader",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Justin M.",
    author_email="thisisjustinm@outlook.com",
    url="https://github.com/thisisjustinm/",
    license="MIT",
    install_requires=['requests','argparse','validators','tqdm'],
    entry_points = {
        'console_scripts': [
            'jget = jget.jget:main',
        ],
    }
)
