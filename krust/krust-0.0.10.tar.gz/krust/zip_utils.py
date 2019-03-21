# -*- coding:utf-8 -*-

import six
import os
from zipfile import ZipFile
from krust.file_utils import MKDIR, DIRNAME, BASENAME, LS_R


def zip(folder, dest, zip_folder=None, ignore_hidden=True):
    """
    Zip a folder into a zip file.
    :param folder: source folder to zip
    :param dest: zip file name
    :param zip_folder: if provided, create a top-level folder in the zip file, whereinto source folder's contents are copied; else, contents of source folder are copied into the zip file directly without a top-level folder; if is True, use the source folder's name.
    :param ignore_hidden:
    :return: dest
    """
    fnames = LS_R(folder, with_root=False, ignore_hidden=ignore_hidden)

    if zip_folder is True:
        zip_folder = BASENAME(folder)

    MKDIR(DIRNAME(dest))
    with ZipFile(dest, 'w', allowZip64=True) as outzip:
        for fname in fnames:
            if zip_folder:
                arcname = os.path.join(zip_folder, fname)
            else:
                arcname = fname
            outzip.write(os.path.join(folder, fname), arcname=arcname)

    return dest


def unzip(fname, dest=None):
    """
    Unzip a zip file into dest.
    :param fname:
    :param dest:
    :return:
    """
    with ZipFile(fname) as f:
        f.extractall(path=dest)

    return dest

