"""Constants definitions."""

import os
from glob import glob
import inspect
from tkinter import ttk
from PIL import ImageTk, Image

BG_COLOR = '#%02x%02x%02x' % (220, 218, 213)
WIDTH_UNIT = 400
BASE_DIR = inspect.getfile(inspect.currentframe())
BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))


class SetException(Exception):
    """Define an exception on the widget setters."""


class GetException(Exception):
    """Define an exception on the widget getters."""


def load_icons():
    """Load icons.

    Load all ./otinker_images/*_icon.gif as icons

    Returns :
    ---------
    load_icons : dictionnary of ImageTk objects
    """
    icons_dir = os.path.join(BASE_DIR, 'images')
    icons_pattern = '_icon.gif'
    icons_files = glob('%s/*%s' % (icons_dir, icons_pattern))
    icons = dict()
    for k in icons_files:
        key = os.path.basename(k).replace(icons_pattern, '')
        icons[key] = ImageTk.PhotoImage(Image.open(k))
    return icons
