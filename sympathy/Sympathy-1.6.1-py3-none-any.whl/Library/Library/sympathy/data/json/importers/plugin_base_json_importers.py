# Copyright (c) 2018, System Engineering Software Society
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the System Engineering Software Society nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL SYSTEM ENGINEERING SOFTWARE SOCIETY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from __future__ import (print_function, division, unicode_literals,
                        absolute_import)
import os
import io
import json
import xmltodict
from sympathy.api import importers
from sympathy.api.exceptions import SyDataError
from sympathy.api import qt as qt_compat

QtGui = qt_compat.import_module('QtGui')


def _sniff_type(filename):
    """
    Guess if it is a JSON or XML file by looking
    at the file extension or the first line
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".json", ".xml"]:
        return ext[1:]

    with open(filename, "rb") as f:
        for line in f:
            line = line.lstrip()
            if line:
                if line.startswith(b"<"):
                    return "xml"
                else:
                    return "json"


def import_data(obj, filename, filetype):
    """
    Load a Json structure from a datasource or a filepath

    :param datasource: the datasource or the filepath to load the Json from
    :param filetype: can be either ``json`` or ``xml`` and determines what type
                     of file to load
    """
    filetype = filetype.lower()
    with io.open(filename, "rb") as f:
        if filetype == "json":
            _dict = json.load(f)
        elif filetype == "xml":
            _dict = xmltodict.parse(f.read())
        else:
            assert False, 'Unknown filetype'
    obj.set(_dict)


class DataImportAuto(importers.JsonDataImporterBase):
    IMPORTER_NAME = "Auto"

    def __init__(self, fq_infilename, parameters):
        self.__importer_class = None
        super(DataImportAuto, self).__init__(fq_infilename, parameters)

    def _importer_class(self):
        if self._fq_infilename is not None:
            if self.__importer_class is None:
                self.__importer_class = (
                    importers.plugin_for_file(
                        importers.JsonDataImporterBase,
                        self._fq_infilename))
        return self.__importer_class

    def valid_for_file(self):
        return False

    def is_type(self):
        importer_class = self._importer_class()
        if importer_class is None:
            raise SyDataError(
                "No importer could automatically be found for this file.")
        importer = importer_class(self._fq_infilename, None)
        return importer.is_type()

    def parameter_view(self, parameters):
        importer_class = self._importer_class()
        if importer_class is None:
            text = "No importer could automatically be found for this file."
        else:
            text = "This file will be imported using the {} importer.".format(
                importer_class.display_name())
        return QtGui.QLabel(text)

    def import_data(self, out_datafile, parameters=None, progress=None):
        importer_class = self._importer_class()

        if importer_class is None:
            raise SyDataError(
                "No importer could automatically be found for this file.")
        importer = importer_class(self._fq_infilename, parameters)
        importer.import_data(out_datafile, parameters, progress)


class DataImportXml(importers.JsonDataImporterBase):
    IMPORTER_NAME = "XML"

    def valid_for_file(self):
        try:
            return _sniff_type(self._fq_infilename) == 'xml'
        except Exception:
            return False

    def parameter_view(self, parameters):
        if not self.valid_for_file():
            return QtGui.QLabel(
                'File does not exist or cannot be read.')
        return QtGui.QLabel()

    def import_data(self, out_datafile, parameters=None, progress=None):
        import_data(out_datafile, self._fq_infilename, filetype='xml')


class DataImportJson(importers.JsonDataImporterBase):
    IMPORTER_NAME = "JSON"

    def valid_for_file(self):
        try:
            return _sniff_type(self._fq_infilename) == 'json'
        except Exception:
            return False

    def parameter_view(self, parameters):
        if not self.valid_for_file():
            return QtGui.QLabel(
                'File does not exist or cannot be read.')
        return QtGui.QLabel()

    def import_data(self, out_datafile, parameters=None, progress=None):
        import_data(out_datafile, self._fq_infilename, filetype='json')
