"""Data modules

This package contains image examples used in tutorials and notebooks.
"""

import os

# Inspired by https://github.com/scikit-image/scikit-image/blob/master/skimage/data/__init__.py
data_dir = os.path.abspath(os.path.dirname(__file__))

__all__ = ['lst']

def fits_gen(instrument_str, particle=None):
    FILE_EXT = (".fits", ".fit")

    particle = "" if particle is None else particle

    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)

        name = file_name.lower()
        start_str = instrument_str + "_" + particle

        if os.path.isfile(file_path) and name.endswith(FILE_EXT) and name.startswith(start_str):
            yield file_path


def lst(ids=None, particle="gamma"):
    """A tuple of FITS files paths containing simulated LST images.

    Often used for tutorials and examples.

    Parameters
    ----------
    ids : a tuple of files name or None
        The selection of FITS files to return.
        Returns the path of all LST images if `ids` is set to `None` (default behavior).

    Returns
    -------
    str or list of str
        The path of the selected FITS files.
    """
    if ids is None:
        return list(fits_gen("lst", particle=particle))
    else:
        path_list = []
        for file_path in fits_gen("lst", particle=particle):
            if os.path.splitext(os.path.basename(file_path))[0] in ids:
                path_list.append(file_path)
        return path_list
