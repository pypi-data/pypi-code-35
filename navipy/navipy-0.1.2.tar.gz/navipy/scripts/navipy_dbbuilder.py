import argparse
import pandas as pd
import numpy as np
import cv2
import os


def parser_navipy_dbbuilder():
    # Create command line options

    description = 'Navipy dbbuilder allow the user to  '
    description += 'generate a database from a list of images '
    description += 'and a csv file containing image name and '
    description += 'position-orientation.'
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    arghelp = 'Folder for the images'
    parser.add_argument('-f', '--folder',
                        required=True,
                        help=arghelp)
    arghelp = 'Path to the csv files containing posorient and image name'
    parser.add_argument('-p', '--posorient',
                        required=True,
                        help=arghelp)
    arghelp = 'Path to the database'
    parser.add_argument('--output-file',
                        require=True,
                        help=arghelp)
    return parser


def main():
    # Fetch arguments
    args = vars(parser_navipy_dbbuilder().parse_args())
    print(args)
    print('End')


if __name__ == "__main__":
    # execute only if run as a script
    main()
