#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import os
import pathlib

# TESTDATA = os.path.join(os.path.dirname(__file__), "test_hmtphenome", "HG00119_filt.vcf")
# print(TESTDATA)
# print(os.path.dirname(__file__))
#
# FIXTURE_DIR = os.path.join(
#     os.path.dirname(os.path.realpath(__file__)),
#     "test_hmtphenome",
#     )
#
# print(FIXTURE_DIR)
#
# p = pathlib.Path(__file__)
# NEW_DIR = p.resolve().parent.joinpath("test_files")
#
# TEST_DIR = os.path.dirname(os.path.realpath(__file__))
# FIXTURE_DIR = os.path.join(TEST_DIR, 'test_hmtnote')
# FIXTURE_FILES = [os.path.join(FIXTURE_DIR, name) for name in ['HG00119_filt.vcf']]
#
# print(TEST_DIR)
# print(FIXTURE_DIR)
# print(FIXTURE_FILES)
# print(NEW_DIR)

HMTNOTE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
print(os.path.dirname(os.path.normpath(HMTNOTE_DIR)))
print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                   "hmtnote", "hmtnote.py"))
