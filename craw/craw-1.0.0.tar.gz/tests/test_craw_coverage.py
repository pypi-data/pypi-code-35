###########################################################################
#                                                                         #
# This file is part of Counter RNAseq Window (craw) package.              #
#                                                                         #
#    Authors: Bertrand Neron                                              #
#    Copyright (c) 2017-2019  Institut Pasteur (Paris).                          #
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

import shutil
import tempfile
import os
from builtins import type
from itertools import zip_longest
import argparse
import sys
import pysam

import craw
from craw.scripts import craw_coverage as craw_cov
from tests import CRAWTest


class TestCoverage(CRAWTest):

    def setUp(self):
        tmp_dir = tempfile.gettempdir()
        self.out_dir = os.path.join(tmp_dir, 'test_craw')
        if os.path.exists(self.out_dir) and os.path.isdir(self.out_dir):
            shutil.rmtree(self.out_dir)
        os.makedirs(self.out_dir)
        self.bin = 'craw_coverage'


    def tearDown(self):
        try:
            shutil.rmtree(self.out_dir)
            pass
        except:
            pass


    def test_positive_int(self):
        self.assertEqual(craw_cov.positive_int(3), 3)

        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            craw_cov.positive_int('Foo')
        self.assertEqual(str(ctx.exception), "must be a positive integer, got: Foo")

        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            craw_cov.positive_int(-1)
        self.assertEqual(str(ctx.exception), "must be a positive integer, got: -1")


    def test_quality_checker(self):
        self.assertEqual(craw_cov.quality_checker(3), 3)

        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            craw_cov.quality_checker('Foo')
        self.assertEqual(str(ctx.exception), "must be a integer between 0 and 42, got: Foo")

        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            craw_cov.quality_checker(-1)
        self.assertEqual(str(ctx.exception), "must be a integer between 0 and 42, got: -1")

        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            craw_cov.quality_checker(45)
        self.assertEqual(str(ctx.exception), "must be a integer between 0 and 42, got: 45")


    def test_get_result_header(self):
        header = """# Running Counter RnAseq Window craw_coverage
#
# Version: craw {cr_ver} | Python {py}
# Using:
#    - pysam {pysam} (samtools {sam})
#    - scipy {scipy} (only for --justify opt)
#
# craw_coverage run with the following arguments:
# --after=3
# --annot=tests/data/annotation_wo_start.txt
# --bam=tests/data/small.bam
# --before=5
# --chr-col=chromosome
# --output=foo.cov
# --qual-thr=0
# --quiet=1
# --ref-col=Position
# --sense=mixed
# --sep=\t
# --strand-col=strand
# --suffix=cov
# --verbose=0
sense\tname\tgene\tchromosome\tstrand\tPosition\t-5\t-4\t-3\t-2\t-1\t0\t1\t2\t3""".format(
            cr_ver=craw.__version__,
            py='{}.{}'.format(sys.version_info.major, sys.version_info.minor),
            pysam=pysam.__version__,
            sam=pysam.__samtools_version__,
            scipy=craw.coverage.scipy.__version__)

        args = argparse.Namespace()
        args.bam = 'tests/data/small.bam'
        args.annot = 'tests/data/annotation_wo_start.txt'
        args.ref_col = 'Position'
        args.before = 5
        args.after = 3
        args.qual_thr = 0
        args.quiet = 1
        args.output = 'foo.cov'
        args.justify = False
        args.sum = False
        args.start_col = False
        args.chr_col = 'chromosome'
        args.sense = 'mixed'
        args.sep = '\t'
        args.strand_col = 'strand'
        args.suffix = 'cov'
        args.verbose = 0

        annot = self.fake_annotation_parser(['name', 'gene', 'chromosome', 'strand', 'Position'], (0, 0))
        self.maxDiff = None

        self.assertEqual(craw_cov.get_result_header(annot, args),
                         header.rstrip())

    def test_get_version_message(self):
        msg = """craw {cr_ver} | Python {py}
Using:
   - pysam {pysam} (samtools {sam})
   - scipy {scipy} (only for --justify opt)
""".format(cr_ver=craw.__version__,
           py='{}.{}'.format(sys.version_info.major, sys.version_info.minor),
           pysam=pysam.__version__,
           sam=pysam.__samtools_version__,
           scipy=craw.coverage.scipy.__version__)

        self.assertEqual(craw_cov.get_version_message(),
                         msg)

    def test_get_results_file(self):
        try:
            sense, antisense = craw_cov.get_results_file('S', os.path.join(self.out_dir, 'foo'), 'cov')
            sense_file_name = os.path.join(self.out_dir, 'foo.sense.cov')
            self.assertTrue(os.path.exists(
                sense_file_name)
            )
            self.assertEqual(sense.name, sense_file_name)
            self.assertEqual(antisense.name, os.devnull)
        finally:
            sense.close()
            antisense.close()
            self.tearDown()

        try:
            self.setUp()
            sense, antisense = craw_cov.get_results_file('AS', os.path.join(self.out_dir, 'foo'), 'cov')
            antisense_file_name = os.path.join(self.out_dir, 'foo.antisense.cov')
            self.assertTrue(os.path.exists(
                antisense_file_name)
            )
            self.assertEqual(sense.name, os.devnull)
            self.assertEqual(antisense.name, antisense_file_name)
        finally:
            sense.close()
            antisense.close()
            self.tearDown()

        try:
            self.setUp()
            sense, antisense = craw_cov.get_results_file('split', os.path.join(self.out_dir, 'foo'), 'cov')
            sense_file_name = os.path.join(self.out_dir, 'foo.sense.cov')
            antisense_file_name = os.path.join(self.out_dir, 'foo.antisense.cov')
            self.assertTrue(os.path.exists(
                sense_file_name)
            )
            self.assertTrue(os.path.exists(
                antisense_file_name)
            )
            self.assertEqual(sense.name, sense_file_name)
            self.assertEqual(antisense.name, antisense_file_name)
        finally:
            sense.close()
            antisense.close()
            self.tearDown()

        try:
            self.setUp()
            sense, antisense = craw_cov.get_results_file('mixed', os.path.join(self.out_dir, 'foo'), 'cov')
            output_file_name = os.path.join(self.out_dir, 'foo.cov')
            self.assertTrue(os.path.exists(
                output_file_name)
            )
            self.assertEqual(sense.name, output_file_name)
            self.assertIs(antisense, sense)
        finally:
            sense.close()
            antisense.close()
            self.tearDown()


    def test_parse_args(self):
        args = {'bam': 'small.bam',
                'annot': 'annotation_wo_start.txt',
                'ref_col': 'Position',
                'before': 5,
                'after': 3,
                'qual_thr': 0,
                'output': 'result_path'}
        command = "--bam {bam} --annot {annot} --before={before} --after={after} " \
                  "--ref-col={ref_col} --qual-thr={qual_thr} --quiet --output={output} ".format(**args)
        self.check_args(args, command)

        args = {'bam': 'small.bam',
                'annot': 'annotation_wo_start_chr_strand_col.txt',
                'ref_col': 'Position',
                'chr_col': 'chr',
                'strand_col': 'brin',
                'before': 5,
                'after': 3,
                'qual_thr': 0,
                'output': 'test_result_path'
                }
        command = "--bam={bam} --annot={annot} --chr-col={chr_col} " \
                  "--strand-col={strand_col} --before={before} --after={after} --ref-col={ref_col} " \
                  "--qual-thr={qual_thr} --quiet --output={output}"
        self.check_args(args, command)

        args = {'bam': 'small.bam',
                'annot': 'annotation_w_start.txt',
                'ref_col': 'Position',
                'start_col': 'beg',
                'stop_col': 'end',
                'qual_thr': 15,
                'output': 'result_path'}

        command = "--bam={bam} --annot={annot} " \
                  "--ref-col={ref_col} --start-col={start_col} --stop-col={stop_col} " \
                  "--qual-thr={qual_thr} --quiet --output={output}"
        self.check_args(args, command)

        args = {'wig': 'small_fixed.wig',
                'annot': 'annotation_4_wig_fixed_win.txt',
                'ref_col': 'Position',
                'before': 5,
                'after': 3,
                'qual_thr': 0,
                'output': 'result_path'}
        command = "--wig={wig} --annot={annot} --before={before} --after={after} " \
                  "--ref-col={ref_col} --qual-thr={qual_thr} --quiet --output={output} "
        self.check_args(args, command)

        args = {'wig': 'small_fixed.wig',
                'annot': 'annotation_4_wig_fixed_win.txt',
                'ref_col': 'Position',
                'window': 5,
                'qual_thr': 0,
                'output': 'result_path'}
        command = "--wig={wig} --annot={annot} --window={window} " \
                  "--ref-col={ref_col} --qual-thr={qual_thr} --quiet --output={output} "
        self.check_args(args, command)

        command = "--annot=annot_file --before=3 --after=5 --ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "At least one of these options must be specified "
                                             "'--bam', '--wig' , '--wig-for', '--wig-rev'.")

        command = "--wig=wig --bam=bam --wig-for=wig_for --wig-rev=wig_rev --annot=annot_file " \
                  "--before=3 --after=5 --ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception),
                         "'--bam', '--wig' , '--wig-for', '--wig-rev' cannot specify at the same time.")

        command = "--wig=wig --bam=bam --annot=annot_file " \
                  "--before=3 --after=5 --ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "'--bam' option cannot be specified in the same time as "
                                             "'--wig', '--wig-for' or '--wig-rev' options.")

        command = "--wig=wig --wig-for=wig_for --wig-rev=wig_rev --annot=annot_file " \
                  "--before=3 --after=5 --ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "'--wig' option cannot be specified in the same time as "
                                             "'--wig-for' or '--wig-rev' options.")

        command = "--wig=wig --annot=annot_file " \
                  "--ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "[--window or [--before, --after] or [--start-col, --stop-col] options "
                                             "must be specified")

        command = "--wig=wig --annot=annot_file " \
                  "--window=5 --before=3 --after=5 --ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "options [--before, --after] and --window are mutually exclusives.")

        command = "--wig=wig --annot=annot_file --after=3 --start-col=start --stop-col=stop " \
                  "--ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "Options [--before, --after, --window] and [--start-col, --stop-col] "
                                             "are mutually exclusives.")

        command = "--wig=wig --annot=annot_file --after=3 " \
                  "--ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "The two options --after and --before work together. "
                                             "The both options must be specified in same time")

        command = "--wig=wig --annot=annot_file --start-col=start " \
                  "--ref-col=Position --qual-thr=0 --quiet --output=output"
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_cov.parse_args(command.split())
        self.assertEqual(str(ctx.exception), "The two options --start-col and --stop-col work together. "
                                             "The both options must be specified in same time")


    def check_args(self, args, tpl):
        command = tpl.format(**args)
        got_args = craw_cov.parse_args(command.split())
        for opt in args:
            self.assertEqual(getattr(got_args, opt), args[opt])


    def test_bam_with_fixed_window(self):
        output_filename = 'small.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)

        args = {'bam': os.path.join(self._data_dir, 'small.bam'),
                'annot': os.path.join(self._data_dir, 'annotation_wo_start.txt'),
                'ref_col': 'Position',
                'before': 5,
                'after': 3,
                'qual_thr': 0,
                'output': test_result_path}
        command = "--bam {bam} --annot {annot} --before={before} --after={after} " \
                  "--ref-col={ref_col} --qual-thr={qual_thr} --quiet --output={output} ".format(**args)
        craw_cov.main(command.split())

        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_bam_with_chr_strand_col(self):
        output_filename = 'coverage_fix_window_chr_strand_col.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        args = {'bam': os.path.join(self._data_dir, 'small.bam'),
                'annot': os.path.join(self._data_dir, 'annotation_wo_start_chr_strand_col.txt'),
                'ref_col': 'Position',
                'chr_col': 'chr',
                'strand_col': 'brin',
                'before': 5,
                'after': 3,
                'qual_thr': 0,
                'output': test_result_path
                }
        command = "--bam={bam} --annot={annot} --chr-col={chr_col} " \
                  "--strand-col={strand_col} --before={before} --after={after} --ref-col={ref_col} " \
                  "--qual-thr={qual_thr} --quiet --output={output}".format(**args)

        craw_cov.main(command.split())

        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_bam_with_var_window(self):
        output_filename = 'coverage_var_window.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        args = {'bam': os.path.join(self._data_dir, 'small.bam'),
                'annot': os.path.join(self._data_dir, 'annotation_w_start.txt'),
                'ref_col': 'Position',
                'start_col': 'beg',
                'stop_col': 'end',
                'qual_thr': 15,
                'output': test_result_path
                }
        command = "--bam={bam} --annot={annot} " \
                  "--ref-col={ref_col} --start-col={start_col} --stop-col={stop_col} " \
                  "--qual-thr={qual_thr} --quiet --output={output}".format(**args)

        craw_cov.main(command.split())

        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_wig_with_fixed_window(self):
        output_filename = 'wig_fixed_window.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        args = {'wig': os.path.join(self._data_dir, 'small_fixed.wig'),
                'annot': os.path.join(self._data_dir, 'annotation_4_wig_fixed_win.txt'),
                'ref_col': 'Position',
                'before': 5,
                'after': 3,
                'qual_thr': 0,
                'output': test_result_path}
        command = "--wig={wig} --annot={annot} --before={before} --after={after} " \
                  "--ref-col={ref_col} --qual-thr={qual_thr} --quiet --output={output}".format(**args)
        craw_cov.main(command.split())

        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_wig_with_var_window(self):
        output_filename = 'wig_var_window.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--wig={wig_file} --annot={annot_file} " \
                  "--ref-col={ref_col} --start-col={start_col} --stop-col={stop_col} " \
                  "--qual-thr={qual} --quiet --output={out_file} ".format(
                                                wig_file=os.path.join(self._data_dir, 'small_variable.wig'),
                                                annot_file=os.path.join(self._data_dir, 'annotation_4_wig_var_win.txt'),
                                                ref_col='Position',
                                                start_col='beg',
                                                stop_col='end',
                                                qual=15,
                                                out_file=test_result_path
                                                )

        craw_cov.main(command.split())

        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_2wig_with_fixed_window(self):
        """
        """
        output_filename = 'wig_splited_fixed_window.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--wig-for={wig_for} --wig-rev={wig_rev} --annot={annot_file} " \
                  "--before={before} --after={after} --ref-col={ref_col} " \
                  "--qual-thr={qual}  --quiet " \
                  "--output={out_file} ".format(wig_for=os.path.join(self._data_dir, 'small_fixed.wig'),
                                                wig_rev=os.path.join(self._data_dir, 'small_fixed_reverse.wig'),
                                                annot_file=os.path.join(self._data_dir, 'annotation_4_wig_fixed_win.txt'),
                                                ref_col='Position',
                                                before=5,
                                                after=3,
                                                qual=0,
                                                out_file=test_result_path
                                                )
        craw_cov.main(command.split())
        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_only_forward_wig(self):
        """
        """
        output_filename = 'wig_only_forward.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--wig-for={wig_for} --annot={annot_file} " \
                  "--before={before} --after={after} " \
                  "--ref-col={ref_col} --qual-thr={qual} " \
                  "--quiet --output={out_file} ".format(
                                                        wig_for=os.path.join(self._data_dir, 'small_fixed.wig'),
                                                        annot_file=os.path.join(self._data_dir, 'annotation_4_wig_fixed_win.txt'),
                                                        ref_col='Position',
                                                        before=5,
                                                        after=3,
                                                        qual=0,
                                                        out_file=test_result_path
                                                    )
        craw_cov.main(command.split())
        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()

        self._check_coverage_file(expected_result, test_result)


    def test_only_reverse_wig(self):
        """
        """
        output_filename = 'wig_only_reverse.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--wig-rev={wig_rev} --annot={annot_file} " \
                  "--before={before} --after={after} " \
                  "--ref-col={ref_col} --qual-thr={qual} --quiet " \
                  "--output={out_file} ".format(wig_rev=os.path.join(self._data_dir, 'small_fixed_reverse.wig'),
                                                annot_file=os.path.join(self._data_dir, 'annotation_4_wig_fixed_win.txt'),
                                                ref_col='Position',
                                                before=5,
                                                after=3,
                                                qual=0,
                                                out_file=test_result_path
                                                )
        craw_cov.main(command.split())
        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()

        self._check_coverage_file(expected_result, test_result)


    def test_resized_var_window(self):
        """
        """
        output_filename = 'wig_var_window_justify.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--wig={wig_file} --annot={annot_file} " \
                  "--ref-col={ref_col} --start-col={start_col} --stop-col={stop_col} " \
                  "--qual-thr={qual} --quiet --output={out_file} " \
                  "--justify 10".format(wig_file=os.path.join(self._data_dir, 'small_variable.wig'),
                                        annot_file=os.path.join(self._data_dir, 'annotation_4_wig_var_win.txt'),
                                        ref_col='Position',
                                        start_col='beg',
                                        stop_col='end',
                                        qual=15,
                                        out_file=test_result_path
                                        )
        craw_cov.main(command.split())
        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def test_sum_var_window(self):
        """
        """
        output_filename = 'wig_var_window_sum.cov'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--wig={wig_file} --annot={annot_file} " \
                  "--ref-col={ref_col} --start-col={start_col} --stop-col={stop_col} " \
                  "--qual-thr={qual} --quiet --output={out_file} " \
                  "--sum".format(wig_file=os.path.join(self._data_dir, 'small_variable.wig'),
                                 annot_file=os.path.join(self._data_dir, 'annotation_4_wig_var_win.txt'),
                                 ref_col='Position',
                                 start_col='beg',
                                 stop_col='end',
                                 qual=15,
                                 out_file=test_result_path
                                 )
        craw_cov.main(command.split())
        expected_result_path = os.path.join(self._data_dir, output_filename)
        with open(expected_result_path) as expected_result_file:
            expected_result = expected_result_file.readlines()

        with open(test_result_path) as test_result_file:
            test_result = test_result_file.readlines()
        self._check_coverage_file(expected_result, test_result)


    def _check_coverage_file(self, expected_result, test_result):
        for expected, result in zip_longest(expected_result, test_result, fillvalue=''):
            if expected.startswith("# Version:"):
                continue
            elif expected.startswith("#    - pysam"):
                continue
            elif expected.startswith("#    - scipy"):
                continue
            elif expected.startswith("# --annot="):
                continue
            elif expected.startswith("# --bam="):
                continue
            elif expected.startswith("# --wig="):
                continue
            elif expected.startswith("# --wig-for="):
                continue
            elif expected.startswith("# --wig-rev="):
                continue
            elif expected.startswith("# --output="):
                continue
            else:
                self.assertEqual(expected, result)


    def fake_annotation_parser(self, header, max):
        return type("AnnotationParser",
                    (object,),
                    {"header": header,
                     "max": lambda: max})
