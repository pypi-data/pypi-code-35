# /********************************************************************************
# * Copyright © 2018-2019, ETH Zurich, D-BSSE, Andreas P. Cuny & Gotthold Fläschner
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the GNU Public License v3.0
# * which accompanies this distribution, and is available at
# * http://www.gnu.org/licenses/gpl
# *
# * Contributors:
# *     Andreas P. Cuny - initial API and implementation
# *******************************************************************************/

from pyIMD.error.error_handler import ArgumentError

__author__ = 'Andreas P. Cuny'


def write_to_png(plot_object, file, **kwargs):
    """Method to write figures in png format to current directory

    Args:
        plot_object (`ggplot obj`):   ggplot object
        file (`str`):                 File path + file name of the figure to save

    Keyword Args:
         width (`int`):               Figure width (optional)
         height (`int`):              Figure height (optional)
         units (`str`):               Figure units (optional) 'in', 'mm' or 'cm'
         resolution (`int`):          Figure resolution in dots per inch [dpi] (optional)

    Returns:
           png file (`void`):         Writes figure to disk as png
    """
    if 'width' and 'height' and 'units' and 'resolution' in kwargs:
        width = kwargs.get('width')
        height = kwargs.get('height')
        units = kwargs.get('units')
        resolution = kwargs.get('resolution')
        plot_object.save(filename='{}.png'.format(file), width=width, height=height, units=units, dpi=resolution)
    elif not kwargs:
        plot_object.save(filename='{}.png'.format(file))
    else:
        raise ArgumentError(write_to_png.__doc__)


def write_to_pdf(plot_object, file, **kwargs):
    """Method to write figures in pdf format to current directory

    Args:
        plot_object (`ggplot object`):  ggplot object
        file (`str`):                   File path + file name of figure to save

    Keyword Args:
         width (`int`):                 Figure width (optional)
         height (`int`):                Figure height (optional)
         units ('str`):                 Figure units (optional) 'in', 'mm' or 'cm'
         resolution (`int`):            Figure resolution in dots per inch [dpi] (optional)

    Returns:
          pdf file (`void`):            Writes figure to disk as pdf

    """
    if 'width' and 'height' and 'units' and 'resolution' in kwargs:
        width = kwargs.get('width')
        height = kwargs.get('height')
        units = kwargs.get('units')
        resolution = kwargs.get('resolution')
        plot_object.save(filename='{}.pdf'.format(file), width=width, height=height, units=units, dpi=resolution)
    elif not kwargs:
        plot_object.save(filename='{}.pdf'.format(file))
    else:
        raise ArgumentError(write_to_pdf.__doc__)


def write_to_disk_as(file_format, plot_object, file, **kwargs):
    """Method to write figures in various file formats

    Args:
        file_format (`str`):            File format identifier i.e. png or pdf
        plot_object (`ggplot object`):  ggplot object
        file (`str`):                   File path + file name of the figure to save

    Keyword Args:
         width (`int`):                 Figure width (optional)
         height (`int`):                Figure height (optional)
         units ('str`):                 Figure units (optional) 'in', 'mm' or 'cm'
         resolution (`int`):            Figure resolution in dots per inch [dpi] (optional)

    Returns:
          file (`void`):                Writes figure to disk in the respective file format

    """
    if file_format == 'pdf':
        write_to_pdf(plot_object, file, **kwargs)
    elif file_format == 'png':
        write_to_png(plot_object, file, **kwargs)
    else:
        raise Exception("This figure format is currently not supported.")
