""""""

# Standard library modules.
import os
from distutils import dir_util, file_util, log
from distutils.cmd import Command

# Third party modules.
from setuptools import setup, find_packages
import setuptools.command.build_py as _build_py
import tqdm

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class generate_rcc(Command):

    URL_API = 'https://commons.wikimedia.org/w/api.php'
    IMAGE_SIZES = [16, 22, 32]

    description = "Download Tango icons and generate Qt resource file"

    user_options = [
        ('build-lib=', 'd', "directory to \"build\" (copy) to"),
        ]

    def initialize_options(self):
        self.build_lib = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_lib', 'build_lib'))

    def query_wikimedia_image_titles(self, page_title):
        import requests

        def parse_response(response):
            image_titles = []
            for page in response['query']['pages']:
                for imageinfo in response['query']['pages'][page]['images']:
                    image_titles.append(imageinfo['title'])
            return image_titles

        params = {'action': 'query',
                  'titles': page_title,
                  'prop': 'images',
                  'format': 'json',
                  'imlimit': 100}
        response = requests.get(self.URL_API, params=params).json()
        image_titles = parse_response(response)

        while "continue" in response:
            params['imcontinue'] = response['continue']['imcontinue']
            response = requests.get(self.URL_API, params=params).json()
            image_titles += parse_response(response)

        return image_titles

    def query_wikimedia_image_url(self, title):
        import requests

        params = {'action': 'query',
                  'titles': title,
                  'prop': 'imageinfo',
                  'format': 'json',
                  'iiprop': 'url'}
        response = requests.get(self.URL_API, params=params).json()

        pages = list(response['query']['pages'].keys())
        return response['query']['pages'][pages[0]]['imageinfo'][0]['url']

    def download_wikimedia_image(self, url, outdir):
        import requests_download

        _, filename = url.rsplit('/', 1)
        filepath = os.path.join(outdir, filename.lower())

        if not os.path.exists(filepath):
            requests_download.download(url, filepath)

        return filepath

    def download_wikimedia_images(self, page_title, outdir):
        dir_util.mkpath(outdir)

        image_titles = self.query_wikimedia_image_titles(page_title)

        image_filepaths = []

        for image_title in tqdm.tqdm(image_titles, desc='download images'):
            url = self.query_wikimedia_image_url(image_title)
            filepath = self.download_wikimedia_image(url, outdir)
            image_filepaths.append(filepath)

        return image_filepaths

    def create_png(self, filepath, sizes):
        from qtpy import QtGui

        icon = QtGui.QIcon(filepath)

        dirname, basename = os.path.split(filepath)
        basename, _ = os.path.splitext(basename)

        for size in sizes:
            pixmap = icon.pixmap(size, size)

            directory = '{0:d}x{0:d}'.format(size)
            pngfilepath = os.path.join(dirname, directory, basename + '.png')
            dir_util.mkpath(os.path.dirname(pngfilepath))
            pixmap.save(pngfilepath)

    def resize(self, image_filepaths, sizes):
        from qtpy import QtGui

        app = QtGui.QGuiApplication([])

        for image_filepath in tqdm.tqdm(image_filepaths, desc='resize images'):
            self.create_png(image_filepath, sizes)

        app.quit()

    def create_theme(self, outdir, sizes):
        # NOTE: Cannot use configparser because index.theme is case-sensitive

        directories = ['{0:d}x{0:d}'.format(size) for size in sizes]

        lines = ['[Icon Theme]',
                 'Name=tango',
                 'Comment=Original tango icons',
                 'Inherits=default',
                 'Directories=' + ','.join(directories)]

        for size, directory in zip(sizes, directories):
            lines += ['[' + directory + ']',
                      'Size={0:d}'.format(size),
                      '']

        filepath = os.path.join(outdir, 'index.theme')
        with open(filepath, 'w') as fp:
            fp.write('\n'.join(lines))

    def create_qrc(self, outdir, sizes):
        import xml.etree.ElementTree as etree
        import xml.dom.minidom as minidom
        import glob

        root = etree.Element('RCC', version='1.0')
        element_qresource = etree.SubElement(root, 'qresource',
                                             prefix='icons/tango')

        element = etree.SubElement(element_qresource, 'file', alias='index.theme')
        element.text = os.path.abspath(os.path.join(outdir, 'index.theme'))

        for size in sizes:
            directory = '{0:d}x{0:d}'.format(size)
            for filepath in glob.glob(os.path.join(outdir, directory, '*.png')):
                filename = os.path.basename(filepath)
                alias = os.path.join(directory, filename)
                text = os.path.abspath(filepath)
                element = etree.SubElement(element_qresource, 'file', alias=alias)
                element.text = text

        outfilepath = os.path.join(outdir, 'tango.qrc')
        with open(outfilepath, 'w') as fp:
            fp.write(minidom.parseString(etree.tostring(root)).toprettyxml())

    def create_rcc(self, outdir):
        import subprocess

        qrcfilepath = os.path.join(outdir, 'tango.qrc')
        outfilepath = os.path.join(outdir, 'tango.rcc')
        args = ['rcc', '--binary', '-o', outfilepath, '--compress', '9', qrcfilepath]
        subprocess.run(args, check=True)

    def run(self):
        import tempfile

        outdir = os.path.join(tempfile.gettempdir(), 'pyqttango')

        log.info('download images from WikiMedia')
        image_filepaths = self.download_wikimedia_images('Tango_icons', outdir)

        log.info('resize images')
        self.resize(image_filepaths, self.IMAGE_SIZES)

        log.info('create theme')
        self.create_theme(outdir, self.IMAGE_SIZES)

        log.info('create qrc')
        self.create_qrc(outdir, self.IMAGE_SIZES)

        log.info('create rcc')
        self.create_rcc(outdir)

        log.info('copy to build directory')
        src = os.path.join(outdir, 'tango.rcc')
        dst = os.path.join(self.build_lib, 'pyqttango')
        dir_util.mkpath(dst)
        file_util.copy_file(src, dst)

class build_py(_build_py.build_py):

    def run(self):
        self.run_command('generate_rcc')
        super().run()

with open(os.path.join(BASEDIR, 'README.rst'), 'r') as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages()
PACKAGE_DATA = {}

INSTALL_REQUIRES = ['qtpy']
EXTRAS_REQUIRE = {'develop': ['nose', 'coverage', 'requests', 'requests_download', 'tqdm']}

CMDCLASS = versioneer.get_cmdclass()
CMDCLASS['build_py'] = build_py
CMDCLASS['generate_rcc'] = generate_rcc

setup(name="pyqttango",
      version=versioneer.get_version(),
      url='https://github.com/ppinard/pyqttango',
      description="Qt resource file containing Tango freedesktop.org icons",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/x-rst",
      author="Philippe T. Pinard",
      author_email="philippe.pinard@gmail.com",
      license="Apache Software License 2.0",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent'],

      packages=PACKAGES,
      package_data=PACKAGE_DATA,

      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,

      cmdclass=CMDCLASS,

      test_suite='nose.collector',
)

