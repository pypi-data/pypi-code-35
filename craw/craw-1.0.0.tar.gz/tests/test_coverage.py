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


import os
import pysam
import logging
from itertools import zip_longest

from tests import CRAWTest

from craw.wig import Genome, WigParser, _log
import craw.coverage

from craw.annotation import new_entry_type


class TestCoverage(CRAWTest):

    @classmethod
    def setUpClass(cls):
        _log.setLevel(logging.ERROR)

    def test_get_coverage_function(self):
        sam_path = os.path.join(self._data_dir, 'small.bam')
        bam_obj = pysam.AlignmentFile(sam_path, "rb")
        func = craw.coverage.get_raw_coverage_function(bam_obj)
        self.assertEqual(craw.coverage.get_raw_bam_coverage, func)
        genome = Genome()
        func = craw.coverage.get_raw_coverage_function(genome)
        self.assertEqual(func, craw.coverage.get_raw_wig_coverage)
        with self.assertRaises(RuntimeError) as ctx:
            craw.coverage.get_raw_coverage_function('foo')
        self.assertEqual(str(ctx.exception),
                         "get_coverage support only 'wig.Genome' or 'pysam.calignmentfile.AlignmentFile' "
                         "as Input, not str")

    def test_get_raw_bam_coverage(self):
        sam_path = os.path.join(self._data_dir, 'small.bam')
        sam_file = pysam.AlignmentFile(sam_path, "rb")
        annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position']
        entry_cls_name = 'foo'
        ref_col = 'Position'
        ne_class = new_entry_type(entry_cls_name, annot_fields, ref_col)
        value_lines = [['YEL072W', 'RMD6', 'chrV', '+', 14415],
                       ['YEL071W', 'DLD3', 'chrV', '+', 17848],
                       ['YEL071W', 'DLD3', 'chrV', '+', 4],
                       ['YEL077C', 'YEL077C', 'chrV', '-', 262],
                       ]

        expected = [{'for': [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'rev': [0, 0, 0, 0, 0, 0, 0, 0, 0]
                     },
                    {'for': [227, 227, 227, 227, 227, 226, 225, 224, 224],
                     'rev': [0, 0, 0, 0, 0, 0, 0, 0, 0]
                     },
                    {'for': [0, 0, 0, 0, 0, 0, 0],
                     'rev': [0, 0, 0, 0, 0, 0, 0]
                     },
                    {'for': [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     'rev': [12, 12, 12, 12, 12, 12, 12, 12, 8]
                     }
                    ]
        # get_bam_coverage work with 0-based positions
        # whereas annot_entry with 1-based positions
        before = 5
        after = 3
        for values, exp_val in zip(value_lines, expected):
            annot_entry = ne_class([str(v) for v in values])
            if annot_entry.strand == '+':
                start = values[-1] - before - 1
                stop = values[-1] + after
            else:
                start = values[-1] - after - 1
                stop = values[-1] + before
            start = max(start, 0)
            stop = max(stop, 0)
            forward_cov, reverse_cov = craw.coverage.get_raw_bam_coverage(sam_file,
                                                                          annot_entry,
                                                                          start,
                                                                          stop,
                                                                          qual_thr=0)

            self.assertListEqual(forward_cov, exp_val['for'])
            self.assertListEqual(reverse_cov, exp_val['rev'])

    def test_get_raw_bam_coverage_bad_pysam(self):
        class FakeAlignmentFile:
            def __init__(self, *args, **kwargs):
                pass

            def count_coverage(self, *args, **kwarg):
                raise SystemError

        annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position']
        ref_col = 'Position'
        ne_class = new_entry_type('Foo', annot_fields, ref_col)
        annot_entry = ne_class(['YEL072W', 'RMD6', 'chrV', '+', '14415'])
        with self.catch_log():
            with self.assertRaises(SystemError) as ctx:
                craw.coverage.get_raw_bam_coverage(FakeAlignmentFile(),
                                                   annot_entry,
                                                   0,
                                                   3,
                                                   qual_thr=0)


    def test_get_raw_wig_coverage(self):
        wig_parser = WigParser(os.path.join(self._data_dir, 'small_fixed.wig'))
        genome = wig_parser.parse()
        annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position']
        entry_cls_name = 'foo'
        ref_col = 'Position'
        ne_class = new_entry_type(entry_cls_name, annot_fields, ref_col)
        value_lines = [['YEL072W', 'RMD6', 'chrV', '+', 15],
                       ['YEL071W', 'DLD3', 'chrV', '+', 20],
                       ['YEL071W', 'DLD3', 'chrV', '+', 4],
                       ['YEL077C', 'DLD3', 'chrV', '-', 13],
                       ]
        exp_values = [
            {'for': [0., 150., 150., 150., 150., 150., 100., 100., 100.],
             'rev': [0.] * 9
             },
            {'for': [150., 100., 100., 100., 100., 100., 5., 5., 5.],
             'rev': [0.] * 9
             },
            {'for': [0., 0., 0., 0., 0., 0., 0.],
             'rev': [0., 0., 0., 0., 0., 0., 0.]
             },
            {'for': [100., 100., 100., 150., 150., 150., 150., 150., 0.],
             'rev': [0.] * 9
             }
        ]

        before = 5
        after = 3
        for values, exp_val in zip_longest(value_lines, exp_values):
            annot_entry = ne_class([str(v) for v in values])
            # get_wig_coverage work with 0-based positions
            # whereas annot_entry with 1-based positions
            # in annot_entry start and stop are included
            # in get_bam_coverage start is included
            # whereas stop is excluded
            if annot_entry.strand == '+':
                start = (values[-1] - 1) - before
                stop = (values[-1] - 1) + after + 1
            else:
                # if feature is on reverse strand
                # before and after are inverted
                start = (values[-1] - 1) - after
                stop = (values[-1] - 1) + before + 1
            start = max(start, 0)
            stop = max(stop, 0)
            forward_cov, reverse_cov = craw.coverage.get_raw_wig_coverage(genome,
                                                            annot_entry,
                                                            start,
                                                            stop,
                                                            qual_thr=0)
            self.assertListEqual(forward_cov, exp_val['for'])
            self.assertListEqual(reverse_cov, exp_val['rev'])


    def test_get_coverage_padded_var_window(self):
            wig_parser = WigParser(os.path.join(self._data_dir, 'small_variable.wig'))
            genome = wig_parser.parse()
            annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position', 'beg', 'end']
            entry_cls_name = 'foo'
            ref_col = 'Position'
            ne_class = new_entry_type(entry_cls_name, annot_fields, ref_col, start_col='beg', stop_col='end')
            value_lines = [
                           ['YEL072W', 'RMD6', 'chrV', '+', 15, 12, 19],
                           ['YEL071W', 'DLD3', 'chrV', '+', 8, 5, 17],
                           ['YEL077C', '077C', 'chrV', '-', 15, 13, 20]
                           ]

            exp_values = [
                {'for': [None, None, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, None, None, None, None, None],
                 'rev': [None, None, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, None, None, None, None, None]
                 },
                {'for': [None, None, 0, 0, 0, 0, 0, 0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                 'rev': [None, None, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0]
                 },
                {'for': [20.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, None, None, None, None, None, None, None],
                 'rev': [20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0, None, None, None, None, None, None, None]
                 }
                ]
            # get_wig_coverage work with 0-based positions
            # whereas annot_entry with 1-based positions

            get_coverage = craw.coverage.padded_coverage_maker(genome, 5, 9, qual_thr=0)
            for values, exp_val in zip_longest(value_lines, exp_values):
                annot_entry = ne_class([str(v) for v in values])
                # get_bam_coverage work with 0-based positions
                # whereas annot_entry with 1-based positions
                # in annot_entry start and stop are included
                # in get_bam_coverage start is included
                # whereas stop is excluded
                start = annot_entry.start - 1
                stop = annot_entry.stop
                forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)

                self.assertListEqual(forward_cov, exp_val['for'])
                self.assertListEqual(reverse_cov, exp_val['rev'])


    def test_get_coverage_padded_fix_window(self):
        wig_parser = WigParser(os.path.join(self._data_dir, 'small_fixed.wig'))
        genome = wig_parser.parse()
        annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position']
        entry_cls_name = 'foo'
        ref_col = 'Position'
        ne_class = new_entry_type(entry_cls_name, annot_fields, ref_col)
        value_lines = [['YEL072W', 'RMD6', 'chrV', '+', 15],
                       ['YEL071W', 'DLD3', 'chrV', '+', 20],
                       ['YEL071W', 'DLD3', 'chrV', '+', 4],
                       ['YEL077C', 'DLD3', 'chrV', '-', 13],
                       ]
        exp_values = [
            {'for': [0., 150., 150., 150., 150., 150., 100., 100., 100.],
             'rev': [0.] * 9
             },
            {'for': [150., 100., 100., 100., 100., 100., 5., 5., 5.],
             'rev': [0.] * 9
             },
            {'for': [None, None, 0., 0., 0., 0., 0., 0., 0.],
             'rev': [None, None, 0., 0., 0., 0., 0., 0., 0.]
             },
            {'for': [100., 100., 100., 150., 150., 150., 150., 150., 0.],
             'rev': [0.] * 9
             }
        ]

        before = 5
        after = 3
        get_coverage = craw.coverage.padded_coverage_maker(genome, 5, 3, qual_thr=0)
        for values, exp_val in zip_longest(value_lines, exp_values):
            annot_entry = ne_class([str(v) for v in values])
            # get_wig_coverage work with 0-based positions
            # whereas annot_entry with 1-based positions
            # in annot_entry start and stop are included
            # in get_bam_coverage start is included
            # whereas stop is excluded
            if annot_entry.strand == '+':
                start = (values[-1] - 1) - before
                stop = (values[-1] - 1) + after + 1
            else:
                # if feature is on reverse strand
                # before and after are inverted
                start = (values[-1] - 1) - after
                stop = (values[-1] - 1) + before + 1

            forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)
            self.assertListEqual(forward_cov, exp_val['for'])
            self.assertListEqual(reverse_cov, exp_val['rev'])


    def test_get_coverage_sum_window(self):
        wig_parser = WigParser(os.path.join(self._data_dir, 'small_fixed.wig'))
        genome = wig_parser.parse()
        annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position']
        entry_cls_name = 'foo'
        ref_col = 'Position'
        ne_class = new_entry_type(entry_cls_name, annot_fields, ref_col)
        value_lines = [['YEL072W', 'RMD6', 'chrV', '+', 15],
                       ['YEL071W', 'DLD3', 'chrV', '+', 20],
                       ['YEL071W', 'DLD3', 'chrV', '+', 4],
                       ['YEL077C', 'DLD3', 'chrV', '-', 13],
                       ]
        exp_values = [
            {'for': (sum([0., 150., 150., 150., 150., 150., 100., 100., 100.]),),
             'rev': (0.,)
             },
            {'for': (sum([150., 100., 100., 100., 100., 100., 5., 5., 5.]),),
             'rev': (0.,)
             },
            {'for': (0.,),
             'rev': (0.,)
             },
            {'for': (sum([100., 100., 100., 150., 150., 150., 150., 150., 0.]),),
             'rev': (0.,)
             }
        ]

        before = 5
        after = 3
        get_coverage = craw.coverage.sum_coverage_maker(genome, qual_thr=0)
        for values, exp_val in zip_longest(value_lines, exp_values):
            annot_entry = ne_class([str(v) for v in values])
            # get_wig_coverage work with 0-based positions
            # whereas annot_entry with 1-based positions
            # in annot_entry start and stop are included
            # in get_bam_coverage start is included
            # whereas stop is excluded
            if annot_entry.strand == '+':
                start = (values[-1] - 1) - before
                stop = (values[-1] - 1) + after + 1
            else:
                # if feature is on reverse strand
                # before and after are inverted
                start = (values[-1] - 1) - after
                stop = (values[-1] - 1) + before + 1

            forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)
            self.assertTupleEqual(forward_cov, exp_val['for'])
            self.assertTupleEqual(reverse_cov, exp_val['rev'])


    def test_get_coverage_resize_window(self):
        wig_parser = WigParser(os.path.join(self._data_dir, 'small_variable.wig'))
        genome = wig_parser.parse()
        annot_fields = ['name', 'gene', 'chromosome', 'strand', 'Position', 'beg', 'end']
        entry_cls_name = 'foo'
        ref_col = 'Position'
        ne_class = new_entry_type(entry_cls_name, annot_fields, ref_col, start_col='beg', stop_col='end')
        value_line = ['YEL072W', 'RMD6', 'chrV', '+', 15, 12, 19]


        exp_values = {'for': [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                      'rev': [12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]
                     }

        # get_wig_coverage work with 0-based positions
        # whereas annot_entry with 1-based positions


        ###################################
        # keep the number of values as is #
        ###################################
        get_coverage = craw.coverage.resized_coverage_maker(genome, 8)
        annot_entry = ne_class([str(v) for v in value_line])
        # get_bam_coverage work with 0-based positions
        # whereas annot_entry with 1-based positions
        # in annot_entry start and stop are included
        # in get_bam_coverage start is included
        # whereas stop is excluded
        start = annot_entry.start - 1
        stop = annot_entry.stop
        forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)

        self.assertListEqual(forward_cov, exp_values['for'])
        self.assertListEqual(reverse_cov, exp_values['rev'])


        #################################
        # increase the number of values #
        #################################
        exp_values = {'for': [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0],
                      'rev': [12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0]
                     }

        get_coverage = craw.coverage.resized_coverage_maker(genome, 15)
        forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)

        self.assertListEqual(forward_cov, exp_values['for'])
        self.assertListEqual(reverse_cov, exp_values['rev'])

        ###############################
        # reduce the number of values #
        ###############################
        value_line = ['YEL072W', 'RMD6', 'chrV', '+', 15, 12, 18]
        annot_entry = ne_class([str(v) for v in value_line])
        get_coverage = craw.coverage.resized_coverage_maker(genome, 4)
        start = annot_entry.start - 1
        stop = annot_entry.stop
        forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)
        exp_values = {'for': [2.0, 4.0, 6.0, 8.0],
                      'rev': [12.0, 14.0, 16.0, 18.0]
                      }
        self.assertListEqual(forward_cov, exp_values['for'])
        self.assertListEqual(reverse_cov, exp_values['rev'])

        ###########################
        # whit negative positions #
        ###########################
        value_line = ['YEL072W', 'RMD6', 'chrV', '+', 2, -2, 4]
        annot_entry = ne_class([str(v) for v in value_line])
        get_coverage = craw.coverage.resized_coverage_maker(genome, 5)
        start = annot_entry.start - 1
        stop = annot_entry.stop
        forward_cov, reverse_cov = get_coverage(annot_entry, start, stop)
        exp_values = {'for': [.0, .0, .0, .0, 0.],
                      'rev': [1.0, 1.75, 2.5, 3.25, 4.0]
                      }
        self.assertListEqual(forward_cov, exp_values['for'])
        self.assertListEqual(reverse_cov, exp_values['rev'])