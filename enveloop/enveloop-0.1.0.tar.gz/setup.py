from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='enveloop',
    version='0.1.0',

    description='Various utility for handling loops, recursions, etc.',
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/arrrlo/enveloop.git',
    licence='MIT',

    author='Ivan Arar',
    author_email='ivan.arar@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='loop, recursion, infinite-loop',

    packages=find_packages(),
    install_requires=[
        'click~=7.0',
    ],

    project_urls={
        'Source': 'https://github.com/arrrlo/enveloop.git',
    },

    entry_points={
        'console_scripts': [
            'enveloop=enveloop.cli:cli'
        ],
    },
)
