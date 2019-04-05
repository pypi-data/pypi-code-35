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

import shutil
import tempfile
import os
import stat
import argparse
import logging

import PIL
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib as mtp

from tests import CRAWTest
import craw
from craw.scripts import craw_htmp
from unittest import skipIf


class TestCrawHtmp(CRAWTest):

    def setUp(self):
        self.tmp_dir = tempfile.gettempdir()
        self.bin = 'craw_htmp'


    def tearDown(self):
        try:
            shutil.rmtree(self.out_dir)
            logger = logging.getLogger('craw')
            logger.handlers = []
        except:
            pass

    def test_file_readable(self):
        self.assertEqual(craw_htmp._file_readable(__file__), __file__)

        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_htmp._file_readable('nimportnaoik')
        self.assertEqual(str(ctx.exception), "No such file: {}".format('nimportnaoik'))

        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_htmp._file_readable(os.path.dirname(__file__))
        self.assertEqual(str(ctx.exception),
                         "{} is not a regular file".format(os.path.dirname(__file__)))


    @skipIf(os.getuid() == 0, "root have always right to access file")
    def test_file_readable_bad_permission(self):
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.mkdir(self.out_dir)
        file = os.path.join(self.out_dir, 'fake_file')
        open(file, 'w').close()
        os.chmod(file, stat.S_IWUSR)
        with self.assertRaises(argparse.ArgumentError) as ctx:
            craw_htmp._file_readable(file)
        self.assertEqual(str(ctx.exception),
                         "{} is not readable".format(file))


    def test_gene_size_parser(self):
        self.assertListEqual(craw_htmp._gene_size_parser("start,stop"), ['start', 'stop'])
        with self.assertRaises(argparse.ArgumentError):
            craw_htmp._gene_size_parser("start_stop")

        with self.assertRaises(argparse.ArgumentError):
            craw_htmp._gene_size_parser("start,middle,stop")


    def test_size_fig_parser(self):
        self.assertTupleEqual(craw_htmp._size_fig_parser("12x22"), (12, 22))
        self.assertTupleEqual(craw_htmp._size_fig_parser("12x22in"), (12, 22))
        wide, height = craw_htmp._size_fig_parser("12x22cm")
        self.assertAlmostEqual(wide, 4.72, places=2)
        self.assertAlmostEqual(height, 8.66, places=2)
        wide, height = craw_htmp._size_fig_parser("12x22mm")
        self.assertAlmostEqual(wide, 0.472, places=3)
        self.assertAlmostEqual(height, 0.866, places=3)
        self.assertTupleEqual(craw_htmp._size_fig_parser("12x22px"), (0.12, 0.22))
        self.assertEqual(craw_htmp._size_fig_parser("raw"), "raw")

        with self.assertRaises(argparse.ArgumentError):
            craw_htmp._size_fig_parser("12cm")

        with self.assertRaises(argparse.ArgumentError):
            craw_htmp._size_fig_parser("douze_x_vingtcm")

        with self.assertRaises(argparse.ArgumentError):
            craw_htmp._size_fig_parser("-2x22")


    def test_get_version_message(self):
        msg_expected = craw.get_version_message()
        msg_expected += """
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
        get_message = craw_htmp.get_version_message()
        self.assertEqual(msg_expected, get_message)


    def test_parse_args(self):
        output_filename = 'htmp_raw_lin.png'
        test_result_path = os.path.join('result_dir', output_filename)
        command = "--size {size} " \
                  "--out={out_file} " \
                  "--sort-using-col {sort_using_col} " \
                  "-q " \
                  "{cov_file}".format(size='raw',
                                      out_file=test_result_path,
                                      sort_using_col="start",
                                      cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                                      )
        args = craw_htmp.parse_args(command.split())
        expected_args = self.get_expected_htmp_args(size='raw',
                                                    out=test_result_path,
                                                    quiet=1,
                                                    sort_using_col="start",
                                                    cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                                                    )
        for k in expected_args.__dict__:
            self.assertEqual(getattr(args, k), getattr(expected_args, k),
                             msg="for option {}".format(k))


    def test_raw(self):
        """
        | test if returncode of coverage is 0 and
        | then test if the generated file is the same as a reference file
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                              bin=self.bin,
                              size='raw',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        #print("\n@@@", command)

        craw_htmp.main(command.split())

        for sense in ('sense', 'antisense'):
            filename, suffix = os.path.splitext(output_filename)
            filename = "{}.{}{}".format(filename, sense, suffix)
            expected_result_path = os.path.join(self._data_dir, filename)
            expected_img = Image.open(expected_result_path)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)


    def test_raw_log(self):
        """
        | test if returncode of coverage is 0 and
        | then test if the generated file is the same as a reference file
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_log.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='log',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        ##print("\n@@@", command)
        craw_htmp.main(command.split())

        for sense in ('sense', 'antisense'):
            filename, suffix = os.path.splitext(output_filename)
            filename = "{}.{}{}".format(filename, sense, suffix)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img, delta=1.0, msg=sense)


    def test_raw_log_row(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_log+row.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='log+row',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())

        for sense in ('sense', 'antisense'):
            filename, suffix = os.path.splitext(output_filename)
            filename = "{}.{}{}".format(filename, sense, suffix)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)


    def test_raw_lin_row(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin+row.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='row',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())

        for sense in ('sense', 'antisense'):
            filename, suffix = os.path.splitext(output_filename)
            filename = "{}.{}{}".format(filename, sense, suffix)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)


    def test_with_marks(self):
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_log_marks.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--mark -2 red " \
                  "--mark 2 green " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
            size='raw',
            norm='log',
            out_file=test_result_path,
            cov_file=os.path.join(self._data_dir, '4_htmp.cov')
        )
        # print("\n@@@", command)
        craw_htmp.main(command.split())

        for sense in ('sense', 'antisense'):
            filename, suffix = os.path.splitext(output_filename)
            filename = "{}.{}{}".format(filename, sense, suffix)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)

    def test_raw_sense_only(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin+row.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--sense-only " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='row',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())

        sense = 'sense'
        filename, suffix = os.path.splitext(output_filename)
        filename = "{}.{}{}".format(filename, sense, suffix)
        expected_result_path = os.path.join(self._data_dir, filename)
        result_path, suffix = os.path.splitext(test_result_path)
        result_path = "{}.{}{}".format(result_path, sense, suffix)
        expected_img = Image.open(expected_result_path)
        result_img = Image.open(result_path)
        self.assertImageAlmostEqual(expected_img, result_img)
        self.assertFalse(os.path.exists("{}.{}{}".format(result_path, 'antisense', suffix)))


    def test_raw_antisense_only(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin+row.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--antisense-only " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='row',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())

        sense = 'antisense'
        filename, suffix = os.path.splitext(output_filename)
        filename = "{}.{}{}".format(filename, sense, suffix)
        expected_result_path = os.path.join(self._data_dir, filename)
        result_path, suffix = os.path.splitext(test_result_path)
        result_path = "{}.{}{}".format(result_path, sense, suffix)
        expected_img = Image.open(expected_result_path)
        result_img = Image.open(result_path)
        self.assertImageAlmostEqual(expected_img, result_img)
        self.assertFalse(os.path.exists("{}.{}{}".format(result_path, 'sense', suffix)))


    def test_raw_crop(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin_crop'
        ext = '.png'
        test_result_path = os.path.join(self.out_dir, output_filename + ext)
        command = "--size {size} " \
                  "--out={out_file} " \
                  "--crop -2 2 " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())
        for sense in ('sense', 'antisense'):
            filename = "{}.{}{}".format(output_filename, sense, ext)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)

    def test_raw_sort(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin'
        ext = '.png'
        test_result_path = os.path.join(self.out_dir, output_filename + ext)
        command = "--size {size} " \
                  "--out={out_file} " \
                  "--sort-using-col Position " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())
        for sense in ('sense', 'antisense'):
            filename = "{}.{}{}".format(output_filename, sense, ext)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)


    def test_raw_sort_file(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin_sort_file'
        ext = '.png'
        test_result_path = os.path.join(self.out_dir, output_filename + ext)
        command = "--size {size} " \
                  "--out={out_file} " \
                  "--sort-using-file {sort_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              out_file=test_result_path,
                              sort_file=os.path.join(self._data_dir, '4_htmp_sorting_file.txt'),
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        craw_htmp.main(command.split())
        for sense in ('sense', 'antisense'):
            filename = "{}.{}{}".format(output_filename, sense, ext)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)


    def test_raw_no_fmt(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp'
        ext = 'png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='row',
                              out_file=test_result_path,
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        # print("\n@@@", command)
        if 'DISPLAY' in os.environ:
            craw_htmp.main(command.split())
            for sense in ('sense', 'antisense'):
                self.assertTrue(os.path.exists(os.path.join(self.out_dir,
                                                            "{}.{}.{}".format(output_filename, sense, ext))
                                               )
                                )
        else:
            with self.assertRaises(RuntimeError) as ctx:
                craw_htmp.main(command.split())
            self.assertEqual(str(ctx.exception),
                             """
    'DISPLAY' variable is not set (you probably run craw_htmp in non graphic environment)
    So you must specify an output format (add ext to the output file option as 'my_file.png')
    """)

    @skipIf('DISPLAY' not in os.environ, "run in non interactive environment")
    def test_raw_no_out(self):
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        dir_ori = os.getcwd()
        output_filename = '4_htmp'
        # craw_htmp create result_file beside source file if --out is not specify
        shutil.copy(os.path.join(self._data_dir, output_filename + '.cov'),
                    self.out_dir)
        os.chdir(self.out_dir)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--quiet " \
                  "{cov_file}".format(
                              size='raw',
                              norm='row',
                              cov_file=os.path.join(self.out_dir, output_filename + '.cov')
                             )
        # print("\n@@@", command)
        try:
            craw_htmp.main(command.split())
            for sense in ('sense', 'antisense'):
                path = "{}.{}.{}".format(output_filename, sense, 'png')
                self.assertTrue(os.path.exists(path))
        finally:
            os.chdir(dir_ori)


    def test_non_display(self):
        """
        """
        #############################################################
        #  run in not interactive environment
        #############################################################
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_log+row.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                                    size='raw',
                                    norm='log+row',
                                    out_file=test_result_path,
                                    cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                                )
        display = os.environ.get('DISPLAY', None)
        if display:
            del os.environ['DISPLAY']
        # print("\n@@@", command)
        try:
            craw_htmp.main(command.split())
        finally:
            if display:
                os.environ['DISPLAY'] = display

        for sense in ('sense', 'antisense'):
            filename, suffix = os.path.splitext(output_filename)
            filename = "{}.{}{}".format(filename, sense, suffix)
            expected_result_path = os.path.join(self._data_dir, filename)
            result_path, suffix = os.path.splitext(test_result_path)
            result_path = "{}.{}{}".format(result_path, sense, suffix)
            expected_img = Image.open(expected_result_path)
            result_img = Image.open(result_path)
            self.assertImageAlmostEqual(expected_img, result_img)

        #############################################################
        #  use file not compatible with not interactive environment
        #############################################################
        output_filename = 'htmp_raw_log+row.nimpornaoik'
        test_result_path = os.path.join(self.out_dir, output_filename)

        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                                    size='raw',
                                    norm='log+row',
                                    out_file=test_result_path,
                                    cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                                )
        display = os.environ.get('DISPLAY', None)
        if display:
            del os.environ['DISPLAY']
        # print("\n@@@", command)
        try:
            with self.assertRaises(RuntimeError)as ctx:
                craw_htmp.main(command.split())
        finally:
            if display:
                os.environ['DISPLAY'] = display
        self.assertTrue(str(ctx.exception).strip().startswith(
            "The '.nimpornaoik' format is not supported, choose among"
            ))

        #############################################################
        # not interactive environment and no file specified
        #############################################################
        command = "--quiet " \
                  "{cov_file}".format(
                              cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                             )
        #print("\n@@@", command)

        display = os.environ.get('DISPLAY', None)
        if display:
            del os.environ['DISPLAY']
        try:
            with self.assertRaises(RuntimeError)as ctx:
                craw_htmp.main(command.split())
        finally:
            if display:
                os.environ['DISPLAY'] = display
        self.assertEqual(str(ctx.exception).strip(),
                         """
    'DISPLAY' variable is not set (you probably run craw_htmp in non graphic environment)
    So you cannot use interactive output
    please specify an output file (--out).""".strip())


    def test_bad_cmap(self):
        output_filename = 'htmp_raw_log+row.png'
        test_result_path = os.path.join('foo', output_filename)

        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--cmap=nimportnaoik "\
                  "--quiet " \
                  "{cov_file}".format(
                                    size='raw',
                                    norm='log+row',
                                    out_file=test_result_path,
                                    cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                                )
        # print("\n@@@", command)
        with self.assertRaises(RuntimeError)as ctx:
            craw_htmp.main(command.split())
        self.assertTrue(str(ctx.exception).strip().startswith(
            "Colormap nimportnaoik is not recognized. Possible values are:"
            ))

    @skipIf(os.getuid() == 0, 'root has always right write')
    def test_bad_outdir(self):
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        os.chmod(self.out_dir, stat.S_IRUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IROTH)
        output_filename = 'htmp_raw_log+row.png'
        test_result_path = os.path.join(self.out_dir, output_filename)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
            size='raw',
            norm='log+row',
            out_file=test_result_path,
            cov_file=os.path.join(self._data_dir, '4_htmp.cov')
        )
        # print("\n@@@", command)
        with self.catch_log() as log:
            with self.assertRaises(RuntimeError) as ctx:
                craw_htmp.main(command.split(), logger_out=False)
        self.assertEqual(str(ctx.exception), "/tmp/craw_test is not writable")


    def test_output_exists(self):
        """
        """
        self.out_dir = os.path.join(self.tmp_dir, 'craw_test')
        os.makedirs(self.out_dir)
        output_filename = 'htmp_raw_lin+row'
        ext = '.png'
        test_result_path = os.path.join(self.out_dir, output_filename + ext)
        command = "--size {size} " \
                  "--norm {norm} " \
                  "--out={out_file} " \
                  "--quiet " \
                  "{cov_file}".format(
                                    size='raw',
                                    norm='row',
                                    out_file=test_result_path,
                                    cov_file=os.path.join(self._data_dir, '4_htmp.cov')
                                )
        with open(os.path.join(self.out_dir, '{}.sense{}'.format(output_filename, ext)), 'w'):
            pass
        # print("\n@@@", command)
        with self.assertRaises(RuntimeError) as ctx:
            craw_htmp.main(command.split(), logger_out=False)


    def get_expected_htmp_args(self, **kwargs):
        default_args = argparse.Namespace(antisense_only=False,
                                          cmap='Blues',
                                          cov_file=None,
                                          crop=None,
                                          dpi=None,
                                          mark=None,
                                          norm='lin',
                                          out=None,
                                          quiet=0,
                                          sense_on_bottom=False,
                                          sense_on_left=False,
                                          sense_on_right=False,
                                          sense_on_top=False,
                                          sense_only=False,
                                          size=None,
                                          sort_by_gene_size=None,
                                          sort_using_col=False,
                                          sort_using_file=None,
                                          title=None,
                                          verbose=0)
        for k, v in kwargs.items():
            setattr(default_args, k, v)
        return default_args