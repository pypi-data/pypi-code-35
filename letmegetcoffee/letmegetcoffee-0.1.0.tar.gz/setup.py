import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='letmegetcoffee',
    version='0.1.0',
    packages=setuptools.find_packages(),
    url='https://github.com/RoW171/letmegetcoffee',
    license='MIT',
    author="Robin 'r0w' Weiland",
    author_email='robinweiland@gmx.de',
    description='Provides functionality to notify if an exception occurred',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='exception notification',
    py_modules=["letmegetcoffee"],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
)
