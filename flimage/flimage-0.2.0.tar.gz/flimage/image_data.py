from qpimage.image_data import Phase


class Fluorescence(Phase):
    """Dedicated class for fluorescence data

    For fluorescence data, background correction is defined
    by subtracting the background image from the raw image.
    """
