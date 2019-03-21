"""Data modules

This package contains image examples used in tutorials and notebooks.
"""

import os

# Inspired by https://github.com/scikit-image/scikit-image/blob/master/skimage/data/__init__.py
data_dir = os.path.abspath(os.path.dirname(__file__))

__all__ = ['lst']

def fits_gen():
    FILE_EXT = (".fits", ".fit")

    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(FILE_EXT):
            yield file_path


def lst():
    """A tuple of FITS files paths containing simulated LST images.

    Often used for tutorials and examples.

    Returns
    -------
    str or list of str
        The path of the selected FITS files.
    """
    return list(fits_gen())
