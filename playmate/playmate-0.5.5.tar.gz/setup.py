import re
from codecs import open
from setuptools import setup


with open('playmate/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='playmate',
    version=version,
    description='Google Play Store async application scraper',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Gulats/playmate',
    author='Bharat Gulati',
    author_email='bharat.gulati.certi@gmail.com',
    packages=['playmate'],
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'aiodns',
        'aiohttp',
        'beautifulsoup4',
        'cchardet',
        'lxml',
        'pydash'
    ],
)
