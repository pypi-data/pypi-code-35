# Copyright (c) 2013, System Engineering Software Society
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
"""Apply function(s) on Table(s)."""
from __future__ import (print_function, division, unicode_literals,
                        absolute_import)
import sys
import os.path
from collections import OrderedDict

from sympathy.api import fx_wrapper
from sympathy.utils import components
from sympathy.types import types
from sympathy.api import qt2 as qt_compat
from sympathy.platform import os_support as oss
from sympathy.utils import filebase
from sympathy.api import exceptions


QtGui = qt_compat.import_module('QtGui')  # noqa
QtWidgets = qt_compat.import_module('QtWidgets')  # noqa
QtCore = qt_compat.QtCore  # noqa


def functions_filename(datasource):
    """Returns file datasource filename."""
    path = datasource.decode_path()
    if path:
        return os.path.abspath(path)


def _datatype(node_context):
    for port in node_context.definition['ports']['inputs']:
        if port['name'] == 'port2':
            return port['type']
    assert False, 'Required port name "port2" does not exist'


def match_cls(cls, arg_type, multi):
    if multi:
        try:
            arg_type = arg_type[0]
        except Exception:
            return False

    return any([types.match(types.from_string(arg_type_, False), arg_type)
                for arg_type_ in cls.arg_types])


class PyfileWrapper(object):
    """Extract classes that extend a given base class (functions) from a
    python file. Used to extract function names for node_function_selector.
    """

    def __init__(self, env, arg_type, multi):
        arg_type = types.from_string(arg_type)
        if types.generics(arg_type):
            self._classes = {}
        elif env:
            self._classes = components.get_subclasses_env(
                env, fx_wrapper.Fx)
            self._classes = OrderedDict(
                [(k, v) for k, v in self._classes.items()
                 if match_cls(v, arg_type, multi)])
        else:
            self._classes = {}

    def get_class(self, class_name):
        """Retrieve a single class from the supplied python file.
        Raises NameError if the class doesn't exist.
        """
        try:
            return self._classes[class_name]
        except KeyError:
            raise NameError

    def function_names(self):
        """Extract the names of classes that extend the base class in the
        supplied python file.
        """
        # Only select classes that extend the base class
        return list(self._classes.keys())


class FxSelectorGui(QtWidgets.QWidget):
    def __init__(self, node_context, parent=None):
        super(FxSelectorGui, self).__init__(parent)
        self._node_context = node_context
        self._parameters = node_context.parameters
        layout = QtWidgets.QVBoxLayout()

        datasources = self._node_context.input.group('port1')
        self._copy_input = self._parameters['copy_input'].gui()
        layout.addWidget(self._copy_input)

        if datasources:
            self._functions = self._parameters['selected_functions'].gui()
            self._edit = QtWidgets.QPushButton('Edit source file')
            self._edit.setToolTip(
                'Brings up the source file in the system default editor')
            self._edit.setEnabled(datasources[0].is_valid())

            layout.addWidget(self._functions)
            layout.addWidget(self._edit)
            self._edit.clicked[bool].connect(self._edit_source)

        else:
            layout.addWidget(self._parameters['code'].gui())

        self.setLayout(layout)

    @qt_compat.Slot(bool)
    def _edit_source(self, checked):
        fq_functions_filename = functions_filename(
            self._node_context.input['port1'])
        oss.run_editor(fq_functions_filename)


class FxSelector(object):

    def __init__(self):
        self._multi = False

    def exec_parameter_view(self, node_context):
        return FxSelectorGui(node_context)

    def adjust_parameters(self, node_context):
        parameters = node_context.parameters
        datasources = node_context.input.group('port1')
        if datasources:
            function_names = self._available_function_names(node_context)
            parameters['selected_functions'].adjust(function_names)

    def execute(self, node_context, set_progress):
        in_datafile = node_context.input['port2']
        parameters = node_context.parameters
        copy_input = parameters['copy_input'].value
        out_datafile = node_context.output['port3']
        functions = self._selected_functions(node_context)
        calc_count = len(functions)
        if not functions:
            exceptions.sywarn('No calculations selected.')

        tmp_datafile = filebase.empty_from_type(
            in_datafile.container_type)

        if copy_input:
            tmp_datafile.source(in_datafile)

        for i, function in enumerate(functions):
            set_progress(100.0 * i / calc_count)
            _execute(function, in_datafile, tmp_datafile)

        out_datafile.source(tmp_datafile)

    def _available_function_names(self, node_context):
        wrapper = self._get_wrapper(node_context)
        res = []
        if wrapper:
            res = wrapper.function_names()
        return res

    def _get_wrapper(self, node_context):
        datasources = node_context.input.group('port1')
        if datasources:
            if not datasources[0].is_valid():
                return
            fq_functions_filename = functions_filename(datasources[0])
            if not fq_functions_filename:
                return
            env = components.get_file_env(fq_functions_filename)
        else:
            env = components.get_text_env(
                node_context.parameters['code'].value)
        wrapper = PyfileWrapper(
            env,
            arg_type=_datatype(node_context), multi=self._multi)
        return wrapper

    def _selected_functions(self, node_context):
        parameters = node_context.parameters
        wrapper = self._get_wrapper(node_context)
        res = []
        if wrapper:
            available_functions = self._available_function_names(node_context)
            function_names = available_functions

            if node_context.input.group('port1'):
                function_names = (
                    parameters['selected_functions'].selected_names(
                        available_functions))

            res = [wrapper.get_class(f) for f in function_names]
        return res


def _execute(function, in_data, out_data):
    instance = function(in_data, out_data)
    instance.execute()


class FxSelectorList(FxSelector):

    def __init__(self):
        super(FxSelectorList, self).__init__()
        self._multi = True

    def exec_parameter_view(self, node_context):
        return FxSelectorGui(node_context)

    def execute(self, node_context, set_progress):
        input_list = node_context.input['port2']
        parameters = node_context.parameters
        copy_input = parameters['copy_input'].value
        output_list = node_context.output['port3']
        functions = self._selected_functions(node_context)
        if not functions:
            exceptions.sywarn('No calculations selected.')

        n_inputs = len(input_list)
        n_functions = len(functions)

        for i, in_datafile in enumerate(input_list):
            try:
                input_factor = 100. / n_inputs
                set_progress(i * input_factor)

                out_datafile = input_list.create()
                if copy_input:
                    out_datafile.source(in_datafile)

                for j, function in enumerate(functions):
                    func_factor = input_factor / n_functions
                    _execute(function, in_datafile, out_datafile)
                    set_progress(i * input_factor + j * func_factor)

                output_list.append(out_datafile)
            except Exception:
                raise exceptions.SyListIndexError(i, sys.exc_info())
