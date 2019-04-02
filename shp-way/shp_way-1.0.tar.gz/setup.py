import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='shp_way',
    version='1.0',
    packages=setuptools.find_packages(),
    license='Apache',
    long_description=open('README.md').read(),
    url='https://github.com/bbrownrichardson/ShpWay',
    author='Brianna Brown Richardson',
    author_email='bbrownrichardson@gmail.com',
    install_requires=['pyshp', 'shapely', 'matplotlib', 'networkx', 'scipy', 'mplleaflet'],
    )
