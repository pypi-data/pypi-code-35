from setuptools import setup, find_packages

setup(
    name='mobtimer',
    version='1.0',
    description='A simple timer for mob programming.',
    long_description='.',
    long_description_content_type='text/markdown',
    author='Andrei Fokau',
    url='https://github.com/andreif/mobtimer',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'mobtimer = mobtimer:run',
        ],
    },
)
