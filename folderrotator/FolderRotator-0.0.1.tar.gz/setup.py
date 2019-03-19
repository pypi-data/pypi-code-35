from setuptools import setup, find_packages

setup(
    name='FolderRotator',
    version='0.0.1',
    packages=find_packages(),
    author='Kevin Glasson',
    author_email='kevinglasson+folderrotator@gmail.com',
    url='https://github.com/kevinglasson/folder_rotator',
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        "pytest==4.3.",
        "pytest-sugar==0.9.2"
    ],
    python_requires='>3.6'
)
