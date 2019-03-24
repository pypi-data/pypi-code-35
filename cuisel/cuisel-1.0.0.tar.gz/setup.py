from setuptools import setup

setup(
    name='cuisel',
    description='ncurses-based selector',
    long_description='A ncurses-based tool which helps you select items interactively.',
    maintainer='Minglangjun Li <liminglangjun@gmail.com>',
    url='https://github.com/mljli/cuisel',
    license='BSD',
    download_url='https://github.com/mljli/cuisel',
    version='1.0.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Terminals'
    ],
    packages=['cuisel'],
    entry_points='''
        [console_scripts]
        cuisel=cuisel.cli:main
    '''
)
