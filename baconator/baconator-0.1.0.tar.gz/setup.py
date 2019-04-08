import setuptools


with open('README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='baconator',
    use_scm_version=True,
    description='Hollywood-themed random name generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eladkehat/baconator',
    author='Elad Kehat',
    author_email='eladkehat@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Typing :: Typed'
    ],
    keywords='haikunator heroku naming',
    packages=setuptools.find_packages(exclude=['rsc', 'tests']),
    python_requires='>=3.7',
    install_requires=[],
    setup_requires=['setuptools_scm'],
    entry_points={
        'console_scripts': [
            'baconator=baconator:generate'
        ]
    }
)
