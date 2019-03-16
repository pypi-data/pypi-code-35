from setuptools import setup


long_description = ''
# Get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='cakap',
    version='0.4',
    license='GPL',
    long_description=long_description,
    url='https://github.com/iomarmochtar/cakap',
    author='Imam Omar Mochtar',
    author_email='iomarmochtar@gmail.com',
    install_requires=['python-telegram-bot', 'colorlog'],
    packages=['cakap'],
    keywords='Telegram bot framework',
    classifiers=[
    ]
)
