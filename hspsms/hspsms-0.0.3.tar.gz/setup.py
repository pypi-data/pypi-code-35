import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

name = 'hspsms'

setuptools.setup(
    name=name,
    version=__import__(name).__version__,
    author=__import__(name).__author__,
    author_email="pypidev@civilmachines.com",
    description="HSPSMS API Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=__import__(name).__license__,
    url="https://github.com/civilmachines/HSP-SMS-API",
    python_requires="!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, >=3.4",
    install_requires=open('requirements.txt').read().split(),
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP'
    ),
)
