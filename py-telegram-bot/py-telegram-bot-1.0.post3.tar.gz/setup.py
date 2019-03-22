from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='py-telegram-bot',
    version='1.0.post3',
    author='Nix13',
    author_email='nix1304@gmail.com',
    description='Telegram Bots API wrapper.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'pysocks'],
    url='https://gitlab.com/Nix13/telegram-api',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
