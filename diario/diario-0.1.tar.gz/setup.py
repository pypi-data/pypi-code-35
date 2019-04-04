import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read_file(filepath):
    with open(filepath) as f:
        return f.read()

EXCLUDE_FROM_PACKAGES = []

setuptools.setup(
    name='diario',
    version='0.1',
    author='ElevenPaths',
    author_email='innovationlab@11paths.com',
    description='DIARIO SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://diario.e-paths.com/index.html',
    install_requires=read_file('requirements.txt').splitlines(),
    keywords=['sdk', 'api', 'diario'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    zip_safe=False
)
