#! /usr/bin/env python3

###########################################################################
#                                                                         #
# This file is part of Counter RNAseq Window (craw) package.              #
#                                                                         #
#    Authors: Bertrand Neron                                              #
#    Copyright (c) 2017-2019  Institut Pasteur (Paris).                   #
#    see COPYRIGHT file for details.                                      #
#                                                                         #
#    craw is free software: you can redistribute it and/or modify         #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 3 of the License, or    #
#    (at your option) any later version.                                  #
#                                                                         #
#    craw is distributed in the hope that it will be useful,              #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                 #
#    See the GNU General Public License for more details.                 #
#                                                                         #
#    You should have received a copy of the GNU General Public License    #
#    along with craw (see COPYING file).                                  #
#    If not, see <http://www.gnu.org/licenses/>.                          #
#                                                                         #
###########################################################################

import sys
import os
import argparse
import logging

import matplotlib as mtp
import matplotlib.pyplot as plt

import craw


def _file_readable(value):
    """
    check value given by the parser

    :param str value: the value given by the parser for --sort-using-file option
    :return: the normpath of the value
    :raises: ArgumentError if the file does not exists, or is not a file, or not readable
    """
    if not os.path.exists(value):
        raise argparse.ArgumentError(None, "No such file: {}".format(value))
    elif not os.path.isfile(value):
        raise argparse.ArgumentError(None, "{} is not a regular file".format(value))
    elif not os.access(value, os.R_OK):
        raise argparse.ArgumentError(None, "{} is not readable".format(value))
    return os.path.normpath(value)


def _gene_size_parser(value):
    """
    Parse value given by the parser

    :param value: the value given by the parser for --sort-by-gene-size option
    :type value: string
    :return: name of column representing the start of gene, name of the column representing the end of gene
    :rtype: tuple of 2 string
    :raise: :class:`argparse.ArgumentError` object if value cannot be parsed
    """
    # this function is called only if value is provided to sort-by-gene-size option
    rv = value.split(',')
    if len(rv) == 0:
        rv = ['', '']
    elif len(rv) == 2:
        pass
    else:
        raise argparse.ArgumentError(None, "--sort-by-gene-size {} invalid value. "
                                           "Must be start_col, stop_col (separated by a comma), "
                                           "default= annotation_start,annotation_end".format(value)) from None
    return rv


def _size_fig_parser(value):
    """
    Parse value given by the parser for --size option
    the value must follow the syntax widexheight[unit]
    if the unit is omitted unit is inch
    otherwise unit must be

        * 'mm' for millimeters
        * 'cm' for centimeters
        * 'in' for inches
        * 'px' for pixels

    wide and height must be positive integers.

    :param value: the size of the figure
    :type value: string
    :return: the size in inch ask by the user
    :rtype: tuple of float
    :raise: :class:`argparse.ArgumentError` object
    """
    def mm2in(value):
        return value * (1 / 25.4)

    def cm2in(value):
        return mm2in(value * 10)

    def px2in(value):
        dpi = plt.rcParams['figure.dpi']
        return value / dpi

    err_msg = """--size {} invalid value.
                 The value must be widexheight[unit] or 'raw'.
                 'wide' and 'height' must be positive integers
                 By default unit is in inches.
                 eg: 7x10 or 7x10in for 7 inches wide by 10 inches height
                     70x100mm for 70 mm by 100 mm.
                 default=7x10 or 10x7 depending of the figure orientation."""
    if value == 'raw':
        return 'raw'
    else:
        unit = 'in'
        if value[-2:] in ('mm', 'cm', 'in', 'px'):
            unit = value[-2:]
            value = value[:-2]
        try:
            wide, height = value.split('x')
        except ValueError:
            raise argparse.ArgumentError(None, err_msg.format(value))
        try:
            wide = int(wide)
            height = int(height)
        except ValueError:
            raise argparse.ArgumentError(None, err_msg.format(value))
        if wide < 0 or height < 0:
            raise argparse.ArgumentError(None, err_msg.format(value))

        if unit == 'mm':
            wide = mm2in(wide)
            height = mm2in(height)
        elif unit == 'cm':
            wide = cm2in(wide)
            height = cm2in(height)
        elif unit == 'px':
            wide = px2in(wide)
            height = px2in(height)

        return wide, height


def get_version_message():
    """
    :return: a human readable of craw_htmp version and it's main dependencies.
    :rtype: str
    """
    # pyplot must be import after the argument parsing
    # because in function of the environment ($DYSPLAY and options) the craw_htmp behavior
    # is not the same
    # so heatmap cannot be import before argument parsing
    # so I import the dependencies in get_version_message.
    # it's not very important as get_version_message is called only when --version is set
    # so the program quit after displaying this message.
    import numpy as np
    import pandas as pd
    import matplotlib as mtp
    import PIL
    version_text = craw.get_version_message()
    version_text += """
Using:
   - numpy {np_ver}
   - pandas {pd_ver}
   - matplotlib {mtp_ver}
   - pillow {pil_ver}
""".format(np_ver=np.__version__,
           pd_ver=pd.__version__,
           mtp_ver=mtp.__version__,
           pil_ver=PIL.PILLOW_VERSION
           )
    return version_text


def parse_args(args):
    """
    :param args: the arguments and option as provided by sys.argv without the program name
    :return: the argument parsed
    :rtype: :class:`argparse.Namespace` object
    """
    parser = argparse.ArgumentParser(description="Compute a figure from a file of coverage compute by craw_coverage.py.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(dest="cov_file",
                        help="the path to the coverage file.")

    data_grp = parser.add_argument_group('optional data options')
    data_grp.add_argument("--crop",
                          nargs=2,
                          help="""crop the matrix.
    This option need two values the name of the first and last column to keep
    [start col, stop col] eg --crop -10 1000 .""")

    sort_grp = data_grp.add_mutually_exclusive_group()
    sort_grp.add_argument("--sort-using-col",
                          default=False,
                          help="sort the rows using the column COL.")
    sort_grp.add_argument("--sort-using-file",
                          type=_file_readable,
                          help="""Sort the rows using a file.
    The file must have on the first line the name of the column
    which will use to sort.
    Each following lines must match to a value of this column in the data.""")
    sort_grp.add_argument("--sort-by-gene-size",
                          type=_gene_size_parser,
                          nargs='*',
                          metavar='start_col,stop_col',
                          help="""The rows will be sorted by gene size
    using start-col and stop-col to compute length.
    
    start-col and stop-col must be a string separated by comma.
    If start-col and stop-col are not specified annotation_start and annotation_end
    for start-col and stop-col respectively will be used.
    (Don't put this option without value just before the coverage file.)""")

    matrix_grp = data_grp.add_mutually_exclusive_group()
    matrix_grp.add_argument("--sense-only",
                            action="store_true",
                            default=False,
                            help="Display only sense matrix (default is display both).")
    matrix_grp.add_argument("--antisense-only",
                            action="store_true",
                            default=False,
                            help="Display only anti sense matrix (default is display both).")

    fig_grp = parser.add_argument_group("optional figure options")
    fig_grp.add_argument("--cmap",
                         default="Blues",
                         help="""The color map used to display data.
    The allowed values are defined in
    http:matplotlib.org/examples/color/colormaps_reference.html
    eg: Blues, BuGn, Greens, GnBu, ... (default: Blues).""")
    fig_grp.add_argument("--title",
                         help="""The figure title.
    It will display on the top of the figure.
    (default: the name of the coverage file without extension).""")
    fig_grp.add_argument("--dpi",
                         type=int,
                         help="""The resolution of the output .
    This option work only if --out option is specified with size not raw.
    (default: matplolibrc figure.dpi""")
    fig_grp.add_argument("--size",
                         type=_size_fig_parser,
                         help="""Specify the figure size.
    The value must be widexheight[unit] or 'raw'.
    
    If value is raw it will be produce two image files (for sense and antisense) "
    with one pixel correspond to one coverage value for one nucleotide.
    
    Otherwise, 'wide' and 'height' must be positive integers
    By default units are in inches eg:
    
    * 7x10 or 7x10in for 7 inches wide by 10 inches height
    * 70x100mm for 70 mm by 100 mm.
    
    (default: 7x10 or 10x7 depending of the figure orientation).""")

    fig_grp.add_argument("--norm",
                         choices=["lin", "log", "row", "log+row", "row+log"],
                         default="lin",
                         help="""Which normalization to apply to the data before display them.
    
     * lin a linear normalization is applied on the whole matrix.
     * log a 10 base logarithm will be applied on the data before matrix
       normalization.
     * row mean that a linear normalisation is compute row by row.
     * log+row mean a 10 base logarithm will be applied before a normalisation
       row by row. ('row+log' is an alias for 'log+row').
       (default: lin""")

    fig_grp.add_argument("--mark",
                         action='append',
                         nargs='*',
                         metavar='POS [COLOR]',
                         help="""* POS is mandatory and must be a positive integer.
    * COLOR is optional
      The supported color formats are:
      - Hexadecimal color specifiers, given as '#rgb' or '#rrggbb'. For example, '#ff0000' specifies pure red.
      - Common HTML color names.
    
    If COLOR is omitted the color corresponding to the highest value in the color map (--cmap) will be used.
    (this option cannot be the last one just before the coverage file, on the command line.)""")

    layout = fig_grp.add_mutually_exclusive_group()
    layout.add_argument("--sense-on-left",
                        action="store_true",
                        default=False,
                        help="Where to display the sense matrix relative to antisense matrix (default is top).")
    layout.add_argument("--sense-on-right",
                        action="store_true",
                        default=False,
                        help="Where to display the sense matrix relative to antisense matrix (default is top).")
    layout.add_argument("--sense-on-top",
                        action="store_true",
                        default=False,
                        help="Where to display the sense matrix relative to antisense matrix (default is top).")
    layout.add_argument("--sense-on-bottom",
                        action="store_true",
                        default=False,
                        help="Where to display the sense matrix relative to antisense matrix (default is top).")

    parser.add_argument("--out",
                        help="""The name of the file (the format will based on the extension)
    to save the figure.
    Instead of displaying the figure on the screen, save it directly in this file.
    
    If this option is used with --size raw 2 files will be produced
    for respectively sense and anti sense.
    The extension 'sense' or 'antisense' will be added between the name and the suffix eg:
    --size raw --out foo.png give 2 files 'foo.sense.png' and 'foo.antisense.png'.
    
    If no format (determine using the suffix) is given 'png' will be used.""")

    parser.add_argument("-v", "--verbose",
                        action='count',
                        default=0,
                        help="Increase output verbosity.")
    parser.add_argument("-q", "--quiet",
                        action="count",
                        default=0,
                        help="Reduce output verbosity.")
    parser.add_argument("--version",
                        action='version',
                        version=get_version_message(),
                        help="display the version information and quit.")
    parsed_args = parser.parse_args(args)
    return parsed_args


def main(args=None, log_level=None, logger_out=True):
    """
    The entrypoint for craw_html script

    It will generate a heatmap representing the coverage matrix around the position of interest
    it can display the results on the screen or write it on file depending the options

    :param args: The arguments and option representing the command line
    :type args: list of string
    :param log_level: the level of verbosity
    :param logger_out: True if you want to display logs on stdout, False otherwise
    :return:
    """
    args = sys.argv[1:] if args is None else args
    parsed_args = parse_args(args)

    verbosity = max(logging.INFO + (parsed_args.quiet - parsed_args.verbose) * 10, 1)
    craw.init_logger(verbosity, out=logger_out)

    log = logging.getLogger('craw.htmp')
    log.debug("args={}".format(parsed_args))
    ###########################
    # validating some options #
    ###########################
    # test if DISPlAY
    if not os.environ.get('DISPLAY'):
        if parsed_args.out is not None:
            _, out_format = os.path.splitext(parsed_args.out)
            if not out_format:
                raise RuntimeError("""
    'DISPLAY' variable is not set (you probably run craw_htmp in non graphic environment)
    So you must specify an output format (add ext to the output file option as 'my_file.png')
    """)
            from craw.util import non_interactive_backends
            try:
                backend = non_interactive_backends[out_format.lstrip('.')]
            except KeyError:
                raise RuntimeError("The '{}' format is not supported, choose among {}.".format(
                    out_format,
                    list(non_interactive_backends.keys())
                ))
            mtp.use(backend)
        else:
            raise RuntimeError("""
    'DISPLAY' variable is not set (you probably run craw_htmp in non graphic environment)
    So you cannot use interactive output
    please specify an output file (--out).
    """)

    # the import of pyplot must be done after setting the backend
    import matplotlib.pyplot as plt
    from craw import heatmap

    try:
        color_map = plt.cm.get_cmap(parsed_args.cmap)
    except(AttributeError, ValueError) as err:
        raise RuntimeError("{} : http:matplotlib.org/examples/color/colormaps_reference.html for example".format(err))

    if parsed_args.sort_by_gene_size == []:
        parsed_args.sort_by_gene_size = ['annotation_start', 'annotation_end']
    elif parsed_args.sort_by_gene_size:
        parsed_args.sort_by_gene_size = parsed_args.sort_by_gene_size[0]

    if parsed_args.out:
        out_dir = os.path.dirname(parsed_args.out) or '.'
        if not os.access(out_dir, os.W_OK):
            msg = "{} is not writable".format(out_dir)
            log.error(msg)
            raise RuntimeError(msg)

    log.info("Parsing coverage file")
    data = heatmap.get_data(parsed_args.cov_file)


    def mark_converter(data, marks):
        converted_marks = []
        for value in marks:
            pos = int(value[0])
            color = value[1] if len(value) == 2 else None
            converted_marks.append(heatmap.Mark(pos, data, color_map, color=color))
        return converted_marks

    if parsed_args.mark is not None:
        parsed_args.mark = mark_converter(data, parsed_args.mark)

    sense_data, antisense_data = heatmap.split_data(data)

    if parsed_args.sense_only:
        antisense_data = None
    if parsed_args.antisense_only:
        sense_data = None

    ################
    # sorting data #
    ################
    # if data is empty or data is None sort return data
    # so it's error safe, and not time and space consuming
    if parsed_args.sort_by_gene_size:
        start_col, stop_col = parsed_args.sort_by_gene_size
        sense_data = heatmap.sort(sense_data, 'by_gene_size', start_col=start_col, stop_col=stop_col)
        antisense_data = heatmap.sort(antisense_data, 'by_gene_size', start_col=start_col, stop_col=stop_col)
    elif parsed_args.sort_using_col:
        sense_data = heatmap.sort(sense_data, 'using_col', col=parsed_args.sort_using_col)
        antisense = heatmap.sort(antisense_data, 'using_col', col=parsed_args.sort_using_col)
    elif parsed_args.sort_using_file:
        sense_data = heatmap.sort(sense_data, 'using_file', file=parsed_args.sort_using_file)
        antisense_data = heatmap.sort(antisense_data, 'using_file', file=parsed_args.sort_using_file)

    sense_data = heatmap.remove_metadata(sense_data)
    antisense_data = heatmap.remove_metadata(antisense_data)

    ################
    # croping data #
    ################
    log.info("Croping matrix")
    if parsed_args.crop:
        start_col, stop_col = parsed_args.crop
        sense_data = heatmap.crop_matrix(sense_data, start_col, stop_col)
        antisense_data = heatmap.crop_matrix(antisense_data, start_col, stop_col)

    ####################
    # Normalizing data #
    ####################
    log.info("Normalizing data")

    if parsed_args.norm == "lin":
        log.info("Linear normalisation")
        sense_data = heatmap.lin_norm(sense_data)
        antisense_data = heatmap.lin_norm(antisense_data)
    elif parsed_args.norm == 'log':
        log.info("10 base logarithm normalisation")
        sense_data = heatmap.log_norm(sense_data)
        antisense_data = heatmap.log_norm(antisense_data)
    elif parsed_args.norm == 'row':
        log.info("Linear normalisation by row")
        sense_data = heatmap.lin_norm_row_by_row(sense_data)
        antisense_data = heatmap.lin_norm_row_by_row(antisense_data)
    else:
        # log+row or row+log
        log.info("10 base logarithm and normalisation by row")
        sense_data = heatmap.log_norm_row_by_row(sense_data)
        antisense_data = heatmap.log_norm_row_by_row(antisense_data)

    ##################
    # Drawing figure #
    ##################
    log.info("Drawing figure")
    if parsed_args.size == 'raw':
        # pillow backend
        if parsed_args.sense_only:
            sense_to_compute = ('sense', )
        elif parsed_args.antisense_only:
            sense_to_compute = ('antisense', )
        else:
            sense_to_compute = ('sense', 'antisense')

        if parsed_args.out:
            root_name, im_format = os.path.splitext(parsed_args.out)
            im_format = im_format.lstrip('.')
            if not im_format:
                im_format = 'png'
        else:
            im_format = 'png'
            root_name = os.path.splitext(parsed_args.cov_file)[0]

        out_filename = {}
        for sense in sense_to_compute:
            filename = "{filename}.{sense}.{format}".format(filename=root_name, sense=sense, format=im_format)
            out_filename[sense] = filename
            if os.path.exists(filename):
                msg = "{} already exists".format(filename)
                log.error(msg)
                raise RuntimeError(msg)

        for sense in sense_to_compute:
            log.info("Drawing {}".format(sense))
            data = locals()[sense + '_data']
            if data is not None:
                heatmap.draw_raw_image(data, out_filename[sense], color_map, marks=parsed_args.mark)
            else:
                log.warning("{} data are empty: skip drawing.".format(sense))
    else:
        # matplotlib backend
        ##########
        # layout #
        ##########
        if parsed_args.sense_on_left:
            sense_on = 'left'
        elif parsed_args.sense_on_right:
            sense_on = 'right'
        elif parsed_args.sense_on_top:
            sense_on = 'top'
        elif parsed_args.sense_on_bottom:
            sense_on = 'bottom'
        else:
            sense_on = 'top'

        if parsed_args.title is None:
            title = os.path.basename(os.path.splitext(parsed_args.cov_file)[0])
        else:
            title = parsed_args.title

        fig = heatmap.draw_heatmap(sense_data, antisense_data,
                                   color_map=color_map,
                                   title=title,
                                   sense_on=sense_on,
                                   size=parsed_args.size,
                                   marks=parsed_args.mark)

        if parsed_args.out:
            if os.path.exists(parsed_args.out):
                msg = "The output file: {} already exists.".format(parsed_args.out)
                log.error(msg)
                raise RuntimeError(msg)

            if parsed_args.dpi:
                fig.savefig(parsed_args.out, dpi=parsed_args.dpi)
            fig.savefig(parsed_args.out)
        else:
            plt.show()


if __name__ == '__name__':
    main()
