from setuptools import setup

setup(
    name='python-magic-win64-0.4.15-fork',
    packages=['winmagic'],
    package_dir={'winmagic': 'winmagic'},
    package_data={'winmagic': ['nscaife/*']},
    version='0.4.15',
    install_requires=['python-magic==0.4.15'],
    include_package_data=True,
    description='python-magic-win64 fork for python-magic 0.4.15 bundled with win64 dlls',
    long_description="""This module uses python-magic to access libmagic functionality.
It also distributes and automatically injects the magic library for 64-bit Windows & python.
Can be used as a drop-in replacement for python-magic by using `from winmagic import magic`.
""",
    license='MIT',
    author='Cristian Vîjdea, fork by Jonathan Granskog',
    author_email='cristi@cvjd.me, Jonathan11197@gmail.com',
    url='https://github.com/Jonathan11197/python-magic-win64',
    download_url='https://github.com/Jonathan11197/python-magic-win64/archive/0.4.15.tar.gz',
    keywords=['mime', 'magic', 'file', 'windows', 'win64', 'dll'],  # arbitrary keywords
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
