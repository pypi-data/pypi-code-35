#!/usr/bin/env python
#
# conftest.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import inspect

import ukbparse.fileinfo as fileinfo
import ukbparse.icd10    as icd10


def fake_cache_clear():
    pass


fileinfo.sniff            = inspect.unwrap(fileinfo.sniff)
fileinfo.fileinfo         = inspect.unwrap(fileinfo.fileinfo)
icd10.readICD10CodingFile = inspect.unwrap(icd10.readICD10CodingFile)

fileinfo.sniff           .cache_clear = fake_cache_clear
fileinfo.fileinfo        .cache_clear = fake_cache_clear
icd10.readICD10CodingFile.cache_clear = fake_cache_clear
