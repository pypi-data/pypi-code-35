#! /usr/bin/env python3

###########################################################################
#                                                                         #
# This file is part of Counter RNAseq Window (craw) package.              #
#                                                                         #
#    Authors: Bertrand Neron                                              #
#    Copyright (c) 2017-2019 Institut Pasteur (Paris).                    #
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

import os
import sys
import argparse
import itertools
import logging
import pysam

import craw
from craw.util import progress
from craw import argparse_util
from craw import annotation, coverage
from craw.wig import WigParser


def positive_int(value):
    """
    Parse value given by the parser

    :param value: the value given by the parser
    :type value: string
    :return: the integer corresponding to the value
    :rtype: int
    :raise:  :class:`argparse.ArgumentTypeError`
    """
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer, got: {}".format(value))
    if value < 0:
        msg = "must be a positive integer, got: {}".format(value)
        raise argparse.ArgumentTypeError(msg)
    return value


def quality_checker(value):
    """
    Parse value given by the parser

    :param value: the value given by the parser
    :type value:  string
    :return: the integer >=0 and <=42 corresponding to the value
    :rtype: int
    :raise:  :class:`argparse.ArgumentTypeError` if value does not represent a integer >=0 and <=42
    """

    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a integer between 0 and 42, got: {}".format(value))
    if not 0 <= value <= 42:
        raise argparse.ArgumentTypeError("must be a integer between 0 and 42, got: {}".format(value))
    return value


def get_result_header(annot_parser, parsed_args):
    """
    Compute the header for the results.
    the firts lines start with #
    they contains some general information about the craw (version)
    and options used (for tracbility)
    the last line is the header of columns separated by --sep option
    and can be used as header with pandas

    :param annot_parser: the annotation parser
    :type annot_parser: :class:`annotation.AnnotationParser` object
    :param parsed_args: the command line argument parsed with argparse
    :type parsed_args: :class:`argparse.Namespace`
    :return: The header of the result file
    :rtype: str
    """
    def version_infos():
        header = "# Running Counter RnAseq Window craw_coverage\n"
        commented_ver = get_version_message().rstrip().replace('\n', '\n# ')
        header += """#
# Version: {}
#
# craw_coverage run with the following arguments:
""".format(commented_ver)
        return header

    def options():
        options = ''
        for a, v in sorted(parsed_args.__dict__.items()):
            if v is None or v is False:
                continue
            else:
                if v is True:
                    options += "# --{opt}\n".format(opt=a.replace('_', '-'))
                else:
                    options += "# --{opt}={val}\n".format(opt=a.replace('_', '-'), val=v)
        options.rstrip() + '\n'
        return options

    def padded_header():
        metadata = '\t'.join([str(f) for f in annot_parser.header])
        if parsed_args.start_col:
            max_left, max_right = annot_parser.max()
            pos = '\t'.join(str(p) for p in range(0 - max_left, max_right + 1))
        else:
            pos = '\t'.join(str(p) for p in range(0 - parsed_args.before, parsed_args.after + 1))
        s = "sense\t{metadata}\t{pos}".format(metadata=metadata, pos=pos)
        return s

    def sum_header():
        metadata = '\t'.join([str(f) for f in annot_parser.header])
        return "sense\t{metadata}\tcoverage".format(metadata=metadata)

    def resized_header(new_size):
        metadata = '\t'.join([str(f) for f in annot_parser.header])
        pos = '\t'.join([str(i) for i in range(new_size)])
        return "sense\t{metadata}\t{pos}".format(metadata=metadata, pos=pos)

    header = version_infos()
    header += options()

    if parsed_args.justify:
        header += resized_header(parsed_args.justify)
    elif parsed_args.sum:
        header += sum_header()
    else:
        header += padded_header()
    return header


def get_version_message():
    """
    :return: The human readable CRAW version.
    :rtype: str
    """
    version_text = craw.get_version_message()
    version_text += """
Using:
   - pysam {pysam_ver} (samtools {samtools_ver})
   - scipy {sp_ver} (only for --justify opt)
""".format(pysam_ver=pysam.__version__,
           samtools_ver=pysam.__samtools_version__,
           sp_ver=craw.coverage.scipy.__version__)
    return version_text


def get_results_file(sense_opt, basename, suffix):
    """

    :param str sense_opt: how to managed the sense and antisense results

        * **mixed**: sense and antisense are interleaved in same file
        * **split**: sense and antisense are in separated files
        * **S**: only sense results are write down
        * **AS**: only antisense are write down

    :param str basename: the basename of the results file
    :param str suffix: the suffix of the results file
    :return: the file objects where to write sense and antisense results
    :rtype: tuple (`file object` sense, `file object` antisense)
    """
    if sense_opt == 'S':
        sense_filename = "{filename}.sense.{suffix}".format(filename=basename, suffix=suffix)
        sense = open(sense_filename, 'w')
        antisense = open(os.devnull, 'w')
    elif sense_opt == 'AS':
        sense = open(os.devnull, 'w')
        antisense_filename = "{filename}.antisense.{suffix}".format(filename=basename, suffix=suffix)
        antisense = open(antisense_filename, 'w')
    elif sense_opt == 'split':
        sense_filename = "{filename}.sense.{suffix}".format(filename=basename, suffix=suffix)
        sense = open(sense_filename, 'w')
        antisense_filename = "{filename}.antisense.{suffix}".format(filename=basename, suffix=suffix)
        antisense = open(antisense_filename, 'w')
    else:
        output_filename = "{filename}.{suffix}".format(filename=basename, suffix=suffix)
        sense = open(output_filename, 'w')
        antisense = sense
    return sense, antisense


def parse_args(args):
    """

    :param args: The options set on the command line (without the program name)
    :type args: list of string
    :return:
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    input_grp = parser.add_argument_group()
    input_grp.add_argument("-b", "--bam",
                           help="""The path of the bam file to analyse. 
    --bam option is not compatible with any --wig or --wig-for or --wig-rev options.
    but at least --bam or any of --wig* options is required.""")
    input_grp.add_argument("-w", "--wig",
                           help="""The path of the wig file to analyse.
    The file encode the coverage for the both strand.
    The positive coverage ar on the forward strand whereas the negative coverage a located on the reverse one.
    The --wig option is incompatible with both --bam or --wig-for or --wig-reverse options.""")
    input_grp.add_argument("--wig-for",
                           metavar='FORWARD WIG',
                           help="""The path of a wig file to analyse.
    This file encode the coverage for the forward strand.
    The --wig-for option is incompatible with both --bam or --wig options.""")
    input_grp.add_argument("--wig-rev",
                           metavar='REVERSE WIG',
                           help="""The path of a wig file to analyse.
    This file encode the coverage for the reverse strand.
    The --wig-rev option is incompatible with both --bam or --wig options.""")
    parser.add_argument("-a", "--annot",
                        required=True,
                        help="The path of the annotation file (required).")
    parser.add_argument("--qual-thr",
                        dest='qual_thr',
                        type=quality_checker,
                        default=15,
                        help="The minimal quality of read mapping to take it in account")
    parser.add_argument("-s", "--suffix",
                        default="cov",
                        help="The name of the suffix to use for the output file.")
    parser.add_argument('-o', '--output',
                        dest='output',
                        help="The path of the output (default= base name of annotation file with --suffix)")
    parser.add_argument('--sep',
                        default='\t',
                        help="the separator use to delimit the annotation fields")
    mutually_exclusive_opt = parser.add_mutually_exclusive_group()
    mutually_exclusive_opt.add_argument('--justify',
                                        type=positive_int,
                                        help="to resize all genes coverage to this new size.")
    mutually_exclusive_opt.add_argument('--sum',
                                        action='store_true',
                                        default=False,
                                        help="sum all the coverages on the window.")

    region_grp = parser.add_argument_group(title="region of interest",
                                           description="""Parameters which define regions to compute.

    There is 2 way to define regions:
        * all regions have same length.
        * each region have different lengths.

    In both case a position of reference must be define (--ref-col).

    If all regions have same length:

        --window define the number of nucleotide to take in account before and
          after the reference position (the window will be centered on reference)
        --before define the number of nucleotide to take in account before the
          reference position.
        --after define the number of nucleotide to take in account after the
          reference position.
        --before and --after allow to define non centered window.

        --after and --before options must be set together and are
        incompatible with --window option.

    If all regions have different lengths:

        The regions must be specified in the annotation file.
        --start-col define the name of the column in annotation file which define
          the start position of the region to compute.
        --stop-col define the name of the column in annotation file which define
          the stop position of the region to compute.
    """)
    region_grp.add_argument("--ref-col",
                            default="position",
                            help="The name of the column for the reference position (default: position).")
    region_grp.add_argument("--before",
                            type=positive_int,
                            help="The number of base to compute after the position of reference.")
    region_grp.add_argument("--after",
                            type=positive_int,
                            help="The number of base to compute before the position of reference.")
    region_grp.add_argument("--window",
                            type=positive_int,
                            help="The number of base to compute around the position of reference.")
    region_grp.add_argument("--start-col",
                            help="The name of the column to define the start position.")
    region_grp.add_argument("--stop-col",
                            help="The name of the column to define the stop position.")
    col_name = parser.add_argument_group(title="specify the name of columns")
    col_name.add_argument("--strand-col",
                          default='strand',
                          help="Specify the name of the column representing the strand (default: strand)")
    col_name.add_argument("--chr-col",
                          default='chromosome',
                          help="Specify the name of the column representing the chromosome (default: chromosome)")

    parser.add_argument("--sense",
                        choices=('S', 'AS', 'split', 'mixed'),
                        default='mixed',
                        help="compute result only on: "
                             "sense (S), "
                             "antisense (AS), "
                             "on both senses but produce two separated files (split), "
                             "or in one file (mixed)."
                             "(default: mixed)"
                        )

    parser.add_argument("--version",
                        action=argparse_util.VersionAction,
                        version=get_version_message())
    parser.add_argument("-q", "--quiet",
                        action="count",
                        default=0,
                        help="Reduce verbosity.")
    parser.add_argument("-v", "--verbose",
                        action="count",
                        default=0,
                        help="Increase verbosity.")

    parsed_args = parser.parse_args(args)

    input_opt_group = (parsed_args.bam, parsed_args.wig, parsed_args.wig_for, parsed_args.wig_rev)
    wig_opt_group = (parsed_args.wig, parsed_args.wig_for, parsed_args.wig_rev)

    #############################
    # Check wig and bam options #
    #############################
    if not any(input_opt_group):
        raise argparse.ArgumentError(None, "At least one of these options must be specified"
                                           " '--bam', '--wig' , '--wig-for', '--wig-rev'.")
    elif all(input_opt_group):
        raise argparse.ArgumentError(None,
                                     "'--bam', '--wig' , '--wig-for', '--wig-rev' cannot specify at the same time.")
    elif parsed_args.bam and any(wig_opt_group):
        raise argparse.ArgumentError(None, "'--bam' option cannot be specified in the same time as"
                                           " '--wig', '--wig-for' or '--wig-rev' options.")
    elif parsed_args.wig and any((parsed_args.wig_for, parsed_args.wig_rev)):
        raise argparse.ArgumentError(None, "'--wig' option cannot be specified in the same time as"
                                           " '--wig-for' or '--wig-rev' options.")
    ###########################
    # Checking window options #
    ###########################
    group_one = (parsed_args.before, parsed_args.after, parsed_args.window)
    group_two = (parsed_args.start_col, parsed_args.stop_col)
    if all([v is None for v in itertools.chain(group_one, group_two)]):
        raise argparse.ArgumentError(None, "[--window or [--before, --after] or [--start-col, --stop-col] options"
                                     " must be specified")
    elif any([v is not None for v in group_one]) and any([v is not None for v in group_two]):
        raise argparse.ArgumentError(None, "Options [--before, --after, --window] and [--start-col, --stop-col] "
                                     "are mutually exclusives.")
    elif all([v is None for v in group_two]):
        if parsed_args.window is None:
            if any([v is None for v in (parsed_args.before, parsed_args.after)]):
                raise argparse.ArgumentError(None, "The two options --after and --before work together."
                                             " The both options must be specified in same time")
            else:
                pass
                # window is None, before and after are specify
                # => nothing to do
        else:
            # parsed_args.window is not None:
            if any([v is not None for v in (parsed_args.before, parsed_args.after)]):
                raise argparse.ArgumentError(None, "options [--before, --after] and --window are mutually exclusives.")
            else:
                # --before, --after are None
                parsed_args.before = parsed_args.after = parsed_args.window
    elif not all(group_two):
        raise argparse.ArgumentError(None, "The two options --start-col and --stop-col work together. "
                                     "The both options must be specified in same time")
    return parsed_args


def main(args=None, log_level=None):
    """
    The entrypoint for craw_coverage script
    It will generate a coverage matrix around the position of interest
    and write the results in files

    :param args: the arguments and options given on the command line
    :type args: list of string as given by sys.argv without the program name
    :param log_level: the level of logger
    :type log_level: positive int or logging flag logging.DEBUG, logging.INFO, logging.ERROR, logging.CRITICAL
    """
    args = sys.argv[1:] if args is None else args
    parsed_args = parse_args(args)

    if log_level is None:
        verbosity = max(logging.INFO + (parsed_args.quiet - parsed_args.verbose) * 10, 1)
    else:
        verbosity = log_level
    craw.init_logger(verbosity)

    #######################
    # Parsing input files #
    #######################
    with open(parsed_args.annot) as annot_file:
        annot_line_number = sum(1 for _ in annot_file)
    annot_parser = annotation.AnnotationParser(parsed_args.annot, parsed_args.ref_col,
                                               chr_col=parsed_args.chr_col,
                                               strand_col=parsed_args.strand_col,
                                               start_col=parsed_args.start_col,
                                               stop_col=parsed_args.stop_col,
                                               sep=parsed_args.sep)

    if parsed_args.bam:
        # input_data is a samfile
        input_file = parsed_args.bam
        input_data = pysam.AlignmentFile(parsed_args.bam, "rb")
    elif parsed_args.wig:
        # input_data is a wig.Genome object
        input_file = parsed_args.wig
        wig_parser = WigParser(mixed_wig=parsed_args.wig)
        input_data = wig_parser.parse()
    else:
        # input_data is a wig.Genome object
        input_file = parsed_args.wig_for
        wig_parser = WigParser(for_wig=parsed_args.wig_for, rev_wig=parsed_args.wig_rev)
        input_data = wig_parser.parse()

    annotations = annot_parser.get_annotations()

    ############################
    # checking outputs options #
    ############################
    if not parsed_args.output:
        parsed_args.output = os.path.splitext(input_file)[0]
        out_name = parsed_args.output
        suffix = parsed_args.suffix
    else:
        out_name, suffix = os.path.splitext(parsed_args.output)
        suffix = suffix.strip('.')
        if not suffix:
            suffix = parsed_args.suffix

    sense_file, antisense_file = get_results_file(parsed_args.sense, out_name, suffix)

    ###########################
    # Computing output matrix #
    ###########################
    with sense_file, antisense_file:
        header = get_result_header(annot_parser, parsed_args)

        if parsed_args.sense in ('S', 'split', 'mixed'):
            # if parsed_args.sense is mixed the sense_file and antisense_file are the same object
            print(header, file=sense_file)
        if parsed_args.sense in ('AS', 'split'):
            print(header, file=antisense_file)

        # get the appropriate function according to the input type
        # the 2 functions
        #  - get_wig_coverage
        #  - get_bam_coverage
        # have exactly the same api
        if parsed_args.justify:
            get_coverage = coverage.resized_coverage_maker(input_data, parsed_args.justify, qual_thr=None)
        elif parsed_args.sum:
            get_coverage = coverage.sum_coverage_maker(input_data, qual_thr=parsed_args.qual_thr)
        else:
            if parsed_args.window is not None:
                max_left = max_right = parsed_args.window
            elif parsed_args.before and parsed_args.after:
                max_left = parsed_args.before
                max_right = parsed_args.after
            else:
                max_left, max_right = annot_parser.max()
            get_coverage = coverage.padded_coverage_maker(input_data, max_left, max_right, qual_thr=parsed_args.qual_thr)

        for annot_num, annot_entry in enumerate(annotations, 1):
            if verbosity <= logging.INFO:
                progress(annot_num, annot_line_number)
            if parsed_args.start_col:
                # pos in get_coverage functions are
                # 0 based whereas in annotation they are 1 based
                # start is included, stop is excluded
                start = annot_entry.start - 1
                stop = annot_entry.stop
            else:
                if annot_entry.strand == '+':
                    start = annot_entry.ref - parsed_args.before - 1
                    stop = annot_entry.ref + parsed_args.after
                else:
                    # if  feature is on reverse strand
                    # the before and after are inverted
                    start = annot_entry.ref - parsed_args.after - 1
                    stop = annot_entry.ref + parsed_args.before
            forward_cov, reverse_cov = get_coverage(annot_entry, start=start, stop=stop)

            sens = 'S' if annot_entry.strand == '+' else 'AS'
            if sens == 'S':
                print(sens, annot_entry, *forward_cov, sep='\t', file=sense_file)
            else:
                print(sens, annot_entry, *forward_cov, sep='\t', file=antisense_file)

            sens = 'S' if annot_entry.strand == '-' else 'AS'
            if sens == 'S':
                print(sens, annot_entry, *reverse_cov, sep='\t', file=sense_file)
            else:
                print(sens, annot_entry, *reverse_cov, sep='\t', file=antisense_file)

    print(file=sys.stderr)


if __name__ == '__main__':
    main()
