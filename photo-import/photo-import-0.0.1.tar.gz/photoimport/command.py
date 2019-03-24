"""Photo Import.

Usage:
    photo-import SOURCE DESTINATION

Arguments:
    SOURCE      photo to be imported
    DESTINATION directory to move photos into

Options:
    -h --help       Show this help.
    -v --version    Show version.

"""
import os

from docopt import docopt

from photoimport import __version__
from photoimport.folders import FolderCreator
from photoimport.photos import ExifReader


def main():
    arguments = docopt(__doc__, version=__version__)
    reader = ExifReader(os.path.dirname(arguments['SOURCE']))
    creator = FolderCreator(arguments['DESTINATION'])

    date = reader.extract_date(os.path.basename(arguments['SOURCE']))
    creator.create_folder(date)
    creator.move_file(arguments['SOURCE'], date)
