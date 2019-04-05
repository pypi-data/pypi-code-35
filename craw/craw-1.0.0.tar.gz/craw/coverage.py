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

import logging
import numpy as np
import scipy.interpolate

from pysam import AlignmentFile

from .wig import Genome

_log = logging.getLogger(__name__)


def sum_coverage_maker(input_data, qual_thr=None):
    """
    This function return a new function :func:`get_sum_coverage`

    :param input_data: the input either a samfile (see pysam library) or a genome build from a wig file (see wig module)
    :type input_data: :class:`craw.wig.Genome` or :class:`pysam.AlignmentFile` object
    :param qual_thr: The quality threshold
                    if input data come from wig this parameter is not used,
    :type qual_thr: int
    :return: :func:`get_sum_coverage`, a function which compute the sum of coverage for a gene on each strand
             between position [start, stop[ This function take 3 parameters:

             - **annot_entry**: an entry of the annotation file.
             - **start**: The position to start to compute the coverage(coordinates are 0-based, start position is included).
             - **stop**: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).

             and

             - **return**: a tuple with 2 tuple of float or int representing the coverage on strand forward and reverse.

    :rtype: function
    """
    get_raw_coverage = get_raw_coverage_function(input_data)


    def get_sum_coverage(annot_entry, start, stop):
        if start < 0:
            # if start is negative
            # when start is compute from large window and reads map at the beginning of the reference
            # pysam crash see issue #10
            # and numpy return empty silce
            # So we consider that negative positions (which doe not really exists) have coverage of 0
            start = 0

        covs = get_raw_coverage(input_data, annot_entry, start, stop, qual_thr)
        return tuple([(sum(cov),) for cov in covs])

    return get_sum_coverage


def resized_coverage_maker(input_data, new_size, qual_thr=None):
    """

    :param input_data: the input either a samfile (see pysam library) or a genome build from a wig file (see wig module)
    :type input_data: :class:`craw.wig.Genome` or :class:`pysam.AlignmentFile` object
    :param new_size: the number of values in the coverage vector.
    :type new_size: postive int
    :param qual_thr: The quality threshold
                    if input data come from wig this parameter is not used,
    :type qual_thr: int
    :return: a function :func:`get_resized_coverage`, a function which compute the coverage for a gene on each strand
             between position [start, stop[ This function take 3 parameters:
             the coverage values are generate by linear interpolation from raw values between [start, stop[
             using the scipy.
             see https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.interpolate.interp1d.html

             - **annot_entry**: an entry of the annotation file.
             - **start**: The position to start to compute the coverage(coordinates are 0-based, start position is included).
             - **stop**: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).

             and

             - **return**: a tuple with 2 tuple of float or int representing the coverage on strand forward and reverse.

    :rtype: function
    """
    get_raw_coverage = get_raw_coverage_function(input_data)

    def get_resized_coverage(annot_entry, start, stop):
        """

        :param annot_entry: an entry of the annotation file.
        :type annot_entry: :class:`annotation.Entry` object.
        :param start: The position to start to compute the coverage(coordinates are 0-based, start position is included).
        :type start: int
        :param stop: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).
        :type stop: int
        :return: a new serie with new_size length
        :rtype: list of float instance.
        """
        if start < 0:
            # if start is negative
            # when start is compute from large window and reads map at the beginning of the reference
            # pysam crash see issue #10
            # and numpy return empty silce
            # So we ommit negative value generate new values using real positions
            start = 0
        raw_forward_cov, raw_reverse_cov = get_raw_coverage(input_data, annot_entry, start, stop, qual_thr)
        coverages = []
        serie_len = len(raw_forward_cov)
        for serie in raw_forward_cov, raw_reverse_cov:
            f = scipy.interpolate.interp1d(range(serie_len), serie)
            coverages.append(f(np.linspace(0, serie_len - 1, num=new_size, endpoint=True)).tolist())
        return tuple(coverages)

    return get_resized_coverage


def padded_coverage_maker(input_data, max_left, max_right, qual_thr=None):
    """

    :param input_data: the input either a samfile (see pysam library) or a genome build from a wig file (see wig module)
    :type input_data: :class:`wig.Genome` or :class:`pysam.AlignmentFile` object
    :param max_left: The highest number of base before the reference position to take in account.
    :type max_left: int
    :param max_right: The highest number of base after  the reference position to take in account.
    :type max_right: int
    :param qual_thr: The quality threshold
                    if input data come from wig this parameter is not used,
    :type qual_thr: int
    :return: a function :func:`get_padded_coverage`, a function which compute the coverage for a gene on each strand
             between position *[start, stop[*

             The coverage values are centered on the annot_entry.ref position, the matrix is padded by ``None`` value.::

                [.......[ coverage ref.pos ] .....]
                [....[covergae     ref.pos ] .....]
                [............[ cov ref.pos       ]]

             This function take 3 parameters:

             - **annot_entry**: an entry of the annotation file.
             - **start**: The position to start to compute the coverage(coordinates are 0-based, start position is included).
             - **stop**: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).

             and

             - **return**: a tuple with 2 tuple of float or int representing the coverage on strand forward and reverse.
    :rtype: function
    """
    get_raw_coverage = get_raw_coverage_function(input_data)

    def get_padded_coverage(annot_entry, start, stop):
        """

        :param annot_entry: an entry of the annotation file.
        :type annot_entry: :class:`annotation.Entry` object.
        :param start: The position to start to compute the coverage(coordinates are 0-based, start position is included).
        :type start: int
        :param stop: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).
        :type stop: int
        :return: the coverage for forward and reverse strand padded with ``None``.
        :rtype: tuple of 2 list containing int or float (forward coverage, reverse coverage)
        """
        real_start = start
        pad_neg_start = []
        if start < 0:
            # if start is negative
            # when start is compute from large window and reads map at the beginning of the reference
            # pysam crash see issue #10
            # so we ask coverage from 0 and pad with None value for negative positions
            start = 0
            pad_neg_start = [None] * abs(real_start)

        raw_forward_cov, raw_reverse_cov = get_raw_coverage(input_data, annot_entry, start, stop, qual_thr)

        if annot_entry.strand == '+':
            #  -1 because the ref must not be take in account in pad
            # start and stop are 0 based (see docstring)
            pad_left = [None] * (max_left - (annot_entry.ref - 1 - real_start))
            # but stop is excluded in get_bam and included in annot_entry
            # so it (stop -1) - ( ref -1) => stop -1
            pad_right = [None] * (max_right - (stop - annot_entry.ref))
            pad_left += pad_neg_start
        else:
            pad_left = [None] * (max_left - (stop - annot_entry.ref))
            pad_right = [None] * (max_right - (annot_entry.ref - 1 - real_start))
            pad_right += pad_neg_start
        forward_cov = pad_left + raw_forward_cov + pad_right
        reverse_cov = pad_left + raw_reverse_cov + pad_right
        return forward_cov, reverse_cov
    return get_padded_coverage


def get_raw_coverage_function(input):
    """

    :param input: the input either a samfile (see pysam library) or a genome build from a wig file (see wig module)
    :type input: :class:`wig.Genome` or :class:`pysam.calignmentfile.AlignmentFile` object
    :return: get_wig_coverage or get_bam_coverage according the type of input
    :rtype: function
    :raise RuntimeError: when input is not instance of :class:`pysam.calignmentfile.AlignmentFile` or :class:`wig.Genome`
    """
    if isinstance(input, AlignmentFile):
        return get_raw_bam_coverage
    elif isinstance(input, Genome):
        return get_raw_wig_coverage
    else:
        raise RuntimeError("get_coverage support only 'wig.Genome' or "
                           "'pysam.calignmentfile.AlignmentFile' as Input, not {}".format(input.__class__.__name__))


def get_raw_wig_coverage(genome, annot_entry, start, stop, qual_thr=None):
    """
    :param genome: The genome which store all coverages.
    :type genome: :class:`craw.wig.Genome` object
    :param annot_entry: an entry of the annotation file
    :type annot_entry: :class:`annotation.Entry` object
    :param start: The position to start to compute the coverage(coordinates are 0-based, start position is included).
    :type start: int
    :param stop: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).
    :type stop: int
    :param qual_thr: this parameter is not used, It's here to have the same api as get_bam_coverage.
    :type qual_thr: None
    :return: the coverage (all bases)
    :rtype: tuple of 2 list containing int or float
    """
    chromosome = genome[annot_entry.chromosome]
    forward_cov, reverse_cov = chromosome[start:stop]
    if annot_entry.strand == '-':
        forward_cov.reverse()
        reverse_cov.reverse()
    return forward_cov, reverse_cov


def get_raw_bam_coverage(sam_file, annot_entry, start, stop, qual_thr=15):
    """
    Compute the coverage for a region position by position on each strand

    :param sam_file: the samfile openend with pysam
    :type sam_file: :class:`pysam.AlignmentFile` object.
    :param annot_entry: an entry of the annotation file
    :type annot_entry: :class:`annotation.Entry` object
    :param start: The position to start to compute the coverage(coordinates are 0-based, start position is included).
    :type start: positive int
    :param stop: The position to start to compute the coverage (coordinates are 0-based, stop position is excluded).
    :type stop: positive int
    :param qual_thr: The quality threshold
    :type qual_thr: int
    :return: the coverage (all bases)
    :rtype: tuple of 2 list containing int
    """
    def on_forward(al_seg):
        """
        :param al_seg: a pysam aligned segment (the object used by pysam to represent an aligned read)
        :type al_seg: :class:`pysam.AlignedSegment`
        :return: True if read is mapped to forward strand
        :rtype: boolean
        """
        return not al_seg.is_reverse

    def on_reverse(al_seg):
        """
        :param al_seg: a pysam aligned segment (the object used by pysam to represent an aligned read)
        :type al_seg: :class:`pysam.AlignedSegment`
        :return: True if read is mapped to reverse strand.
        :rtype: boolean
        """
        return al_seg.is_reverse

    def coverage_one_strand(sam_file, chromosome, start, stop, qual, strand):
        """
        Compute the coverage for each position between start and stop on the chromosome on the strand.

        :param sam_file: the sam alignment to use
        :type sam_file: a :class:`pysam.AlignmentFile` object
        :param chromosome: the name of the chromosome
        :type chromosome: basestring
        :param start: The position to start to compute the coverage(coordinates are 0-based, start position is included).
        :type start: int
        :param stop:The position to start to compute the coverage (coordinates are 0-based, stop position is excluded).
        :type stop: int
        :param qual: The quality threshold.
        :type qual: int
        :param strand: the strand on which the read match
        :type strand: string
        :return: the coverage on forward then on reverse strand.
        The coverage is the sum of all kind bases mapped for each position
        :rtype: tuple of 2 list containing int
        """
        call_back = on_forward if strand == '+' else on_reverse

        try:
            coverage = sam_file.count_coverage(chromosome,
                                               start=start,
                                               stop=stop,
                                               quality_threshold=qual,
                                               read_callback=call_back)
        except SystemError as err:
            import sys
            _log.critical("ERROR when call count_coverage with following arguments\n"
                          "reference= {chromosome} \n"
                          "start={start}\n"
                          "end={stop}\n"
                          "quality_threshold={qual}\n"
                          "read_callback={call_back}".format(chromosome=chromosome,
                                                             start=start,
                                                             stop=stop,
                                                             qual=qual,
                                                             call_back=call_back)
                          )
            raise err

        coverage = [array.tolist() for array in coverage]
        window_cov = []
        for cov_A, cov_T, cov_C, cov_G in zip(*coverage):
            window_cov.append(cov_A + cov_T + cov_C + cov_G)
        return window_cov

    forward_cov = coverage_one_strand(sam_file,
                                      annot_entry.chromosome,
                                      start,
                                      stop,
                                      qual_thr,
                                      '+'
                                      )
    reverse_cov = coverage_one_strand(sam_file,
                                      annot_entry.chromosome,
                                      start,
                                      stop,
                                      qual_thr,
                                      '-'
                                      )
    if annot_entry.strand == '-':
        forward_cov.reverse()
        reverse_cov.reverse()
    return forward_cov, reverse_cov

