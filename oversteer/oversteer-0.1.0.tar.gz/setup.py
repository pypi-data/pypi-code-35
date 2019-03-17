from glob import glob
import setuptools
from distutils.command.build import build
from babelglade.translate import translate_desktop_file, translate_appdata_file

class Build(build):
    sub_commands = [('compile_catalog', None)] + build.sub_commands

    def run(self):
        translate_desktop_file('data/org.berarma.Oversteer.desktop.in', 'data/org.berarma.Oversteer.desktop', 'locale')
        translate_appdata_file('data/org.berarma.Oversteer.appdata.xml.in', 'data/org.berarma.Oversteer.appdata.xml', 'locale')
        build.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

mofiles = []
for mofile in glob('locale/*/*/*.mo'):
    mofiles.append(('share/' + mofile, [mofile]))

setuptools.setup(
    name = "oversteer",
    version = "0.1.0",
    author = "Bernat Arlandis",
    author_email = "berarma@hotmail.com",
    description = "Steering Wheel Manager",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/berarma/oversteer",
    packages = ['oversteer'],
    package_dir = {'oversteer':'oversteer'},
    include_package_data = True,
    data_files = [
        ( 'share/applications', ['data/org.berarma.Oversteer.desktop']),
        ( 'share/metainfo', ['data/org.berarma.Oversteer.appdata.xml']),
        ( 'share/icons/hicolor/scalable/apps', ['data/org.berarma.Oversteer.svg']),
        ( 'share/oversteer', ['data/udev/99-logitech-wheel-perms.rules']),
    ] + mofiles,
    exclude_package_data = {
        'oversteer': ['locale/*/*/*.po'],
    },
    install_requires = [
        "pygobject",
        "pyudev",
        "pyxdg",
    ],
    setup_requires=[
        "babel",
        "lxml",
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
    ],
    message_extractors = {
        'oversteer': [
            ('**.py', 'python', None),
            ('**.ui', 'babelglade.extract:extract_glade', None),
        ],
        'resources': [
            ('**.desktop', 'babelglade.extract:extract_desktop', None),
            ('**.appdata.xml', 'babelglade.extract:extract_glade', None),
        ],
    },
    cmdclass = {
        'build': Build,
    },
)
