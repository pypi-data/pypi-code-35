from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='WatchMySASS',
    version='0.1.1',
    description='Compile SCSS inside of HTML files.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Compilers'
    ],
    keywords='SCSS compiler html/scss',
    url='https://github.com/DevonWieczorek/WatchMySASS',
    author='Devon Wieczorek',
    author_email='devon.wieczorek93@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'scss',
        'beautifulsoup4',
        'argparse',
        'watchdog'
    ],
    entry_points = {
        'console_scripts': ['WatchMySASS=WatchMySASS.__init__:main']
    },
    include_package_data=True,
    zip_safe=False
)
