# Copyright (c) 2013, 2017, System Engineering Software Society
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
import operator
import collections
import numpy as np
import sys
import cgi
import ast
from sympathy.api import node as synode
from sympathy.api import table
from sympathy.api import ParameterView
from sympathy.api import qt2 as qt_compat
from sympathy.api.nodeconfig import (
    Port, Ports, Tag, Tags, adjust, deprecated_warn)
from sympathy.api import node_helper
from sympathy.api.exceptions import (SyConfigurationError, SyDataError,
                                     SyUserCodeError)
from sympathy.api import dtypes
from sylib import util

from sympathy.platform.widget_library import BasePreviewTable
from sympathy.platform.table_viewer import TableModel

QtGui = qt_compat.import_module('QtGui')
QtWidgets = qt_compat.import_module('QtWidgets')
QtCore = qt_compat.QtCore

SELECT_WITH_GUI_DOCS = """
Select rows in Tables by applying a constraint to a number of columns in the
incoming Table. The output Table has the selected rows from incoming Table with
order preserved. The number of rows in the output is therefore always less than
or equal to the number of rows in the input. The number of columns is the same.

The constraint can be defined by selecting a comparison operator in the drop
down menu and a entering a constraint value in the text field, the constraint
value will be read as a value of the same type as the column it is compared to.
For information about how to enter text, see :ref:`appendix_typed_text`.
Alternatively a custom filter function can be used.


The constraint will be applied for each selected column. The results per column
are then combined using the selected reduction method. If set to 'all' (the
default) the constraint needs to be True in all selected column for a row to be
included in the output. If set to 'any' it is enough that the constraint is
True for any single selected column. When only one column is selected this
option has no effect.

Rows where any of the selected columns are masked are never included in the
output when not using a custom filter.

A custom filter function can be defined by writing a lambda function. The
lambda function will be called once for each selected column with that
column as a numpy array as argument. The lambda function should return
an array-like object (e.g. `numpy.ndarray` or `pandas.Series`) with boolean
dtype and as many items as there was in the argument.

See https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
for a description of lambda functions. Have a look at the :ref:`Data type
APIs<datatypeapis>` to see what methods and attributes are available on the
data type that you are working with.

Rows where the custom filter that returns a masked array; the rows where
the custom filter is masked will not be included from the output.

"""

SELECT_WITH_TABLE_DOCS = """
Select rows in Table by using an additional Table with predefined comparison
relations. The output Table has the selected rows from incoming Table with
order preserved. The number of rows in the output is therefore always less than
or equal to the number of rows in the input. The number of columns is the same.

The selection Table should have at least three columns that define a set of
constraints. Each row will set up one constraint with a column name, a
comparison operator and a constraint value.

The following operators are recognized by the node, either in their string form
(e.g. ``equal``) or their symbolic form (e.g. ``==``):

    - equal (==)
    - less than (<)
    - less than or equal (<=)
    - greater than (>)
    - greater than or equal (>=)
    - not equal (!=)

Each constraint will be applied in turn. The results per constraint are then
combined using the selected reduction method. If set to *all* (the default) all
the constraint needs to be True for a row to be included in the output. If set
to *any* it is enough any single constraint is True. When the configuration
table only contains a single constraint this option has no effect.  Unless
*Evaluate values as code* is used, each constraint value will be read as a
value of the same type as the column it is compared to. For information about
how to enter text, see :ref:`appendix_typed_text`.



Rows where any of the selected columns are masked are never included in the
output.

Older versions of this node always evaluated the constraint values as Python
code. This behavior is no longer neither encouraged nor default but if you need
it, it can still be enabled by checking the checkbox *Evaluate values as code*.

"""


comparisons = collections.OrderedDict([
    ('equal', '=='),
    ('less than', '<'),
    ('less than or equal', '<='),
    ('greater than', '>'),
    ('greater than or equal', '>='),
    ('not equal', '!=')])


def get_operator(relation):
    if relation in comparisons.keys():
        relation = comparisons[relation]
    elif relation in comparisons.values():
        relation = relation
    else:
        raise SyConfigurationError(
            "Unknown comparison operator: {}".format(relation))
    if relation == '==':
        op = operator.eq
    elif relation == '<':
        op = operator.lt
    elif relation == '<':
        op = operator.lt
    elif relation == '<=':
        op = operator.le
    elif relation == '>':
        op = operator.gt
    elif relation == '>=':
        op = operator.ge
    elif relation == '!=':
        op = operator.ne
    else:
        raise SyConfigurationError(
            "Unknown comparison operator: {}".format(relation))
    return op


def get_predicate(relation, constraint):
    """Return a predicate function defined by relation and constraint."""
    if relation in comparisons.keys():
        comparison = comparisons[relation]
    elif relation in comparisons.values():
        comparison = relation
    else:
        raise SyConfigurationError(
            "Unknown comparison operator: {}".format(relation))
    predicate_fn = 'lambda x: x {} {}'.format(comparison, constraint)
    ctx = {}
    try:
        constraint_value = util.base_eval(constraint, {'x': None})
    except NameError:
        # Assume that the constraint is a string.
        constraint_value = constraint
        ctx = {'constraint_value': constraint_value}
        predicate_fn = 'lambda x: x {0} constraint_value'.format(comparison)
    except Exception:
        # Assume that the constraint depends on x.
        pass
    return util.base_eval(predicate_fn, ctx)


class ParseConstraintError(Exception):
    pass


class ParseCustomError(Exception):
    pass


def _get_constraint_predicate(relation, constraint, constraint_compat):
    op = get_operator(relation)

    def is_nat(value):
        return np.isnat(value)

    def is_not_nat(value):
        return np.logical_not(np.isnat(value))

    def is_nan(value):
        return np.isnan(value)

    def is_not_nan(value):
        return np.logical_not(np.isnan(value))

    def no_cmp_op(value):
        return np.zeros(len(value), dtype=bool)

    def inner(array):
        dtype = array.dtype
        dtype = dtypes.numpy_dtype_factory_for_dtype(dtype)
        cons = constraint

        if dtype.kind in ['U', 'S'] and constraint_compat:
            try:
                cons = ast.literal_eval(cons)
            except Exception:
                pass

        try:
            parsed_constraint = dtypes.numpy_value_from_dtype_str(
                dtype, cons)

        except Exception as e:
            raise ParseConstraintError(', '.join(e.args))

        if parsed_constraint.dtype.kind == 'M':
            if np.isnat(parsed_constraint):
                if op is operator.eq:
                    return is_nat(array)
                elif op is operator.ne:
                    return is_not_nat(array)
                else:
                    no_cmp_op(array)
        elif parsed_constraint.dtype.kind == 'f':
            if np.isnan(parsed_constraint):
                if op is operator.eq:
                    return is_nan(array)
                elif op is operator.ne:
                    return is_not_nan(array)
                else:
                    return no_cmp_op(array)

        return op(array, parsed_constraint)

    return inner


def get_parameter_predicate(parameters):
    """Return a predicate function defined by the node parameters."""
    if parameters['use_custom_predicate'].value:
        try:
            return util.base_eval(parameters['predicate'].value)
        except Exception:
            raise ParseCustomError(sys.exc_info())
    else:
        return _get_constraint_predicate(
            parameters['relation'].selected,
            parameters['constraint'].value,
            parameters['constraint_compat'].value)


def filter_rows_memopt(in_table, out_table, parameters):
    """Update out_table with the filtered rows from in_table."""

    columns = parameters['columns'].selected_names(in_table.names())
    predicate = get_parameter_predicate(parameters)
    nbr_rows = in_table.number_of_rows()

    try:
        exist = parameters['exist'].value.lower()
    except KeyError:
        exist = 'all'

    # Produce selection, a boolean array with same length as in_table
    # indicating which rows to keep.

    if exist == 'all':
        selection = np.ones(nbr_rows, dtype=bool)
    elif exist == 'any':
        selection = np.zeros(nbr_rows, dtype=bool)
    else:
        assert False

    if nbr_rows:
        column_name = None
        try:
            if exist == 'all':
                for column_name in columns:
                    res = predicate(
                        in_table.get_column_to_array(column_name))
                    selection = np.logical_and(selection, res)
            elif exist == 'any':
                for column_name in columns:
                    selection = np.logical_or(selection, predicate(
                        in_table.get_column_to_array(column_name)))
        except ParseConstraintError as e:
            raise SyConfigurationError(
                'In column: {}, failed to parse constraint. {}'
                .format(column_name, e.args[0]))
        except Exception:
            if parameters['use_custom_predicate'].value:
                raise SyUserCodeError(
                    sys.exc_info(),
                    'In column: {}, failed to apply custom filter: {}'.format(
                        column_name, parameters['predicate'].value))
            else:
                raise SyDataError(
                    'In column: {}, failed to compare constraint: {}'.format(
                        column_name, parameters['constraint'].value))

    if isinstance(selection, np.ma.MaskedArray):
        selection = selection.filled(False)

    out_table.update(in_table[np.array(selection)])


class SelectRowsWidget(ParameterView):
    def __init__(self, in_table, parameters, parent=None):
        super().__init__(parent)
        self._in_table = in_table
        self._parameters = parameters
        self._status_message = ''

        vlayout = QtWidgets.QVBoxLayout()

        self._use_custom_predicate_pw = (
            self._parameters['use_custom_predicate'].gui())
        self._predicate_pwidget = (
            self._parameters['predicate'].gui())

        preview_button = QtWidgets.QPushButton("Preview")
        self._preview_table = BasePreviewTable()
        self._preview_table_model = TableModel()
        self._preview_table.setModel(self._preview_table_model)

        limit_label = QtWidgets.QLabel('Previewed rows:')
        self._limit_gui = self._parameters['limit'].gui()
        self.limit_spinbox = self._limit_gui.editor()

        preview_layout = QtWidgets.QHBoxLayout()
        preview_layout.addWidget(preview_button)
        preview_layout.addWidget(limit_label)
        preview_layout.addWidget(self.limit_spinbox)

        vlayout.addWidget(self._parameters['columns'].gui())
        self._exist = self._parameters['exist'].gui()
        vlayout.addWidget(self._exist)
        self._relation = self._parameters['relation'].gui()
        vlayout.addWidget(self._relation)
        self._constraint = self._parameters['constraint'].gui()
        vlayout.addWidget(self._constraint)

        self._constraint_compat = parameters['constraint_compat'].gui()
        vlayout.addWidget(self._constraint_compat)

        vlayout.addWidget(self._use_custom_predicate_pw)
        vlayout.addWidget(self._predicate_pwidget)
        vlayout.addLayout(preview_layout)
        vlayout.addWidget(self._preview_table)

        self._post_init_gui_from_parameters()

        self.setLayout(vlayout)

        self._use_custom_predicate_pw.stateChanged[int].connect(
            self._use_custom_predicate_changed)
        preview_button.clicked[bool].connect(
            self._preview_clicked)
        self._predicate_pwidget.valueChanged[str].connect(
            self._predicate_changed)

    def _post_init_gui_from_parameters(self):
        self._use_custom_predicate_changed()

    def _use_custom_predicate_changed(self):
        use_custom_predicate = (
            self._parameters['use_custom_predicate'].value)
        self._constraint.setEnabled(not use_custom_predicate)
        self._relation.setEnabled(not use_custom_predicate)
        self._constraint_compat.setEnabled(not use_custom_predicate)
        self._predicate_pwidget.setEnabled(use_custom_predicate)

    def _predicate_changed(self):
        color = QtGui.QColor(0, 0, 0, 0)
        try:
            get_parameter_predicate(self._parameters)
        except (SyntaxError, NameError):
            color = QtCore.Qt.red
        except Exception:
            color = QtCore.Qt.red
        palette = self._predicate_pwidget.palette()
        palette.setColor(self._predicate_pwidget.backgroundRole(), color)
        self._predicate_pwidget.setPalette(palette)

    def _preview_clicked(self):
        try:
            in_table = self._in_table['Input']
        except KeyError:
            in_table = None

        out_table = table.File()
        self._status_message = ''
        if in_table.is_valid():

            if in_table is None or in_table.is_empty():
                self._preview_table_model.set_table(table.File())
                return

            limit = self._parameters['limit'].value
            try:
                filter_rows_memopt(in_table, out_table, self._parameters)
                out_table = out_table[:limit]
            except ParseCustomError:
                self._status_message = 'Invalid filter!'
            except Exception as e:
                self._status_message = str(e)
        else:
            self._status_message = 'No input data'

        self.status_changed.emit()
        self._preview_table_model.set_table(out_table)

    @property
    def status(self):
        if self._status_message:
            return '<p>{}</p>'.format(
                cgi.escape(str(self._status_message)))
        return ''


def add_constraint_compat_param(parameters):
    parameters.set_boolean(
        'constraint_compat',
        label='Use compatible string constraints (deprecated)',
        description=(
            'Enable string constraint quote compatibility with older '
            'Sympathy versions. Will be removed in 1.7.0.'))


class SelectRowsOperation(node_helper.TableOperation):
    __doc__ = SELECT_WITH_GUI_DOCS + (
        ":Ref. nodes: "
        ":ref:`Select rows in Table with Table`, "
        ":ref:`Slice data Table`, "
        ":ref:`Filter rows in Table`")

    author = "Alexander Busck"
    version = '1.1'
    description = 'Reduction of rows in Table according to specified filter.'

    icon = 'select_table_rows.svg'
    tags = Tags(Tag.DataProcessing.Select)

    inputs = ['Input']
    outputs = ['Output']
    has_custom_widget = True

    @staticmethod
    def get_parameters(parameter_group):
        editor = synode.Util.multilist_editor(edit=True)
        parameter_group.set_list(
            'columns', label='Columns to filter',
            value=[],
            description='Select columns for comparison relation',
            editor=editor)

        parameter_group.set_string(
            'exist',
            value='all',
            label='Constraint must be satisfied in',
            description=(
                'Constraint must be satisfied in: Any selected column or '
                'All selected columns.'),
            editor=synode.Util.combo_editor(
                options=['all', 'any']))
        parameter_group.set_list(
            'relation', plist=comparisons.keys(),
            label='Relation',
            description='Select comparison operator for relation',
            editor=synode.Util.combo_editor())

        parameter_group.set_string(
            'constraint', label='Filter constraint',
            description='Specify constraint value for comparison relation',
            value='')

        add_constraint_compat_param(parameter_group)

        parameter_group.set_boolean(
            'use_custom_predicate', label='Use custom filter',
            description='Select to use custom filter')

        parameter_group.set_string(
            'predicate', label='Custom filter',
            description='Write a custom filter as a Python lambda function')

        parameter_group.set_integer(
            'limit', label='Preview rows', description='Rows to display',
            editor=synode.Editors.bounded_spinbox_editor(0, 10000, 1),
            value=100)

    def custom_widget(self, in_table, parameters):
        return SelectRowsWidget(in_table, parameters)

    def adjust_table_parameters(self, in_table, parameters):
        try:
            in_data = in_table['Input']
        except KeyError:
            in_data = None
        adjust(parameters['columns'], in_data)

    def execute_table(self, in_table, out_table, parameters):
        """Execute"""
        if (parameters['constraint_compat'].value and
                not parameters['use_custom_predicate'].value):
            deprecated_warn(
                'Support for compatible string constraints',
                '1.7.0',
                "uncheck: 'Use compatible string constraints'")

        in_table = in_table['Input']
        if not in_table.is_empty():
            out_table = out_table['Output']
            try:
                filter_rows_memopt(in_table, out_table, parameters)
            except ParseCustomError as e:
                raise SyUserCodeError(
                    e.arg[0],
                    'Failed to build custom filter.')

            out_table.set_table_attributes(in_table.get_table_attributes())
            out_table.set_name(in_table.get_name())

    def update_parameters(self, parameters):
        if isinstance(self, node_helper.ADAFsCalculation):
            # Workaround for adafs_node_factory.
            try:
                parameters = parameters[node_helper.CHILD_GROUP]
            except KeyError:
                pass

        if 'constraint_compat' not in parameters:
            cons = parameters['constraint'].value
            try:
                cons = ast.literal_eval(cons)
            except Exception:
                pass
            else:
                # cons is a string defined with quotes.
                if isinstance(cons, str) or isinstance(cons, bytes):
                    add_constraint_compat_param(parameters)
                    parameters['constraint_compat'].value = True


SelectTableRows = node_helper.table_node_factory(
    'SelectTableRows', SelectRowsOperation,
    'Select rows in Table',
    'org.sysess.sympathy.data.table.selecttablerows')


SelectTablesRows = node_helper.tables_node_factory(
    'SelectTablesRows', SelectRowsOperation,
    'Select rows in Tables',
    'org.sysess.sympathy.data.table.selecttablerowss')


# This is the only instance, please do not introduce new ones!
SelectADAFsRows = node_helper.adafs_node_factory(
    'SelectADAFsRows', SelectRowsOperation,
    'Select rows in ADAFs',
    'org.sysess.sympathy.data.table.selectadafrows', 'Time series')
SelectADAFsRows.icon = 'select_adaf_rows.svg'


def add_eval_param(parameters):
    parameters.set_boolean(
        'eval', label="Evaluate values as code",
        value=False,
        description=(
            'When checked the values column will be evaluated as Python code. '
            'When unchecked the values column is used as is.'),
        editor=synode.Util.combo_editor())


class SelectTableRowsFromTable(synode.Node):
    __doc__ = SELECT_WITH_TABLE_DOCS + (
        ":Ref. nodes: "
        ":ref:`Select rows in Tables with Table`, "
        ":ref:`Select rows in Table`, "
        ":ref:`Slice data Table`, "
        ":ref:`Filter rows in Table`")

    name = 'Select rows in Table with Table'
    description = ('Select rows in Table by using an additional selection '
                   'Table with predefined comparison relations.')
    icon = 'select_table_rows.svg'

    nodeid = 'org.sysess.sympathy.data.table.selecttablerowsfromtable'
    author = 'Greger Cronquist'
    version = '1.0'
    tags = Tags(Tag.DataProcessing.Select)

    parameters = synode.parameters()
    parameters.set_list(
        'column',
        label="Column with column names",
        description=('Select column in the selection Table that '
                     'includes listed column names.'),
        editor=synode.Util.combo_editor(edit=True, filter=True))
    parameters.set_list(
        'relation',
        label="Column with comparison operators",
        description=('Select column in the selection Table that '
                     'includes listed comparison operators.'),
        editor=synode.Util.combo_editor(edit=True, filter=True))
    parameters.set_list(
        'constraint',
        label="Column with constraint values",
        description=('Select column in the selection Table that '
                     'includes listed constraint values.'),
        editor=synode.Util.combo_editor(edit=True, filter=True))
    parameters.set_list(
        'reduction', label="Reduction:",
        plist=['all', 'any'], value=[0],
        description=(
            'If there are multiple selection criteria, do ALL of them need to '
            'be fulfilled for a data row to be selected, or is it enough that '
            'ANY single criterion is fulfilled?'),
        editor=synode.Util.combo_editor())
    add_eval_param(parameters)

    inputs = Ports([
        Port.Table(
            'Table with three columns that defines a set of comparison '
            'relations. Each row in the set will set up a comparison relation '
            'with a column name, a comparison operator and a constraint '
            'value.',
            name='port1'),
        Port.Table('Input Table', name='port2')])
    outputs = Ports([Port.Table('Table with rows in Selection', name='port1')])

    def update_parameters(self, parameters):
        if 'eval' not in parameters:
            add_eval_param(parameters)
            parameters['eval'].value = True

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['column'],
               node_context.input[0])
        adjust(node_context.parameters['relation'],
               node_context.input[0])
        adjust(node_context.parameters['constraint'],
               node_context.input[0])

    def _generate_selection(self, node_context, tablefile):
        """Return a zip-iterator of the three configuration columns."""
        for param in ['column', 'relation', 'constraint']:
            if not self._parameters[param].selected:
                raise SyConfigurationError('Check configuration parameters.')

        config_table = node_context.input['port1']

        column_names = config_table.get_column_to_array(
            self._parameters['column'].selected)
        relations = config_table.get_column_to_array(
            self._parameters['relation'].selected)
        constraints = config_table.get_column_to_array(
            self._parameters['constraint'].selected)

        self._check_constraint_dtype(constraints)

        new_constraints = []

        if not self._parameters['eval'].value:
            for col_name, constr in zip(column_names, constraints):
                dtype = tablefile.column_type(col_name)
                dtype = dtypes.numpy_dtype_factory_for_dtype(dtype)
                if constraints.dtype.kind in ['U', 'S']:
                    constr = dtypes.numpy_value_from_dtype_str(
                        dtype, constr)
                    new_constraints.append(constr)
                else:
                    new_constraints.append(constr)
        else:
            new_constraints = constraints

        return zip(column_names, relations, new_constraints)

    def _check_constraint_dtype(self, constraint):
        """
        Raise an error if eval is checked and the constraints column has a
        datatype that doesn't work with eval.
        """
        if not self._parameters['eval'].value:
            return

        if constraint.dtype.kind in 'Mm':
            if constraint.dtype.kind == 'M':
                datatype_name = 'datetime'
            elif constraint.dtype.kind == 'm':
                datatype_name = 'timedelta'
            raise SyDataError(
                "Type {} can not be evaluated. Uncheck 'Evaluate values "
                "as code' or use e.g. text type.".format(datatype_name))
        elif constraint.dtype.kind not in 'US':
            deprecated_warn(
                'Support for evaluating columns of types other than text',
                '1.6.0',
                "input of text type or uncheck 'Evaluate values'")

    def _filter_single_file(self, tablefile, node_context):
        """Return a new table with the selected rows from tablefile."""
        indices = []

        for column_name, relation, constraint in self._generate_selection(
                node_context, tablefile):
            if self._parameters['eval'].value:
                deprecated_warn(
                    'Support for evaluating constraints',
                    '1.7.0',
                    "input of text type with suitable read format and uncheck "
                    "'Evaluate values'")

                res = get_predicate(relation, constraint)(
                    tablefile.get_column_to_array(column_name))
            else:
                res = get_operator(relation)(
                    tablefile.get_column_to_array(column_name), constraint)
            if isinstance(res, np.ma.MaskedArray):
                res = res.filled(False)
            indices.append(res)

        if self._parameters['reduction'].selected == 'any':
            index = np.logical_or.reduce(indices)
        else:
            index = np.logical_and.reduce(indices)

        filtered_file = table.File()
        for cname in tablefile.column_names():
            filtered_file.set_column_from_array(
                cname, tablefile.get_column_to_array(cname)[index])

        filtered_file.set_attributes(tablefile.get_attributes())
        return filtered_file

    def execute(self, node_context):
        self._parameters = node_context.parameters

        tablefile = node_context.input['port2']
        if tablefile.is_empty():
            return
        if node_context.input['port1'].is_empty():
            node_context.output['port1'].source(tablefile)
            return
        filtered_table = self._filter_single_file(tablefile, node_context)
        node_context.output['port1'].source(filtered_table)


class SelectTablesRowsFromTable(SelectTableRowsFromTable):
    __doc__ = SELECT_WITH_TABLE_DOCS + (
        ":Ref. nodes: "
        ":ref:`Select rows in Table with Table`, "
        ":ref:`Select rows in Table`, "
        ":ref:`Slice data Table`, "
        ":ref:`Filter rows in Table`")

    name = 'Select rows in Tables with Table'
    description = ('Select rows in Tables by using an additional selection '
                   'Table with predefined comparison relations.')

    nodeid = 'org.sysess.sympathy.data.table.selecttablesrowsfromtable'

    inputs = Ports([Port.Table('Selection', name='port1'),
                    Port.Tables('Input Tables', name='port2')])
    outputs = Ports([Port.Tables(
        'Tables with rows in Selection', name='port1')])

    def execute(self, node_context):
        self._parameters = node_context.parameters

        input_list = node_context.input['port2']
        output_list = node_context.output['port1']

        for tablefile in input_list:
            filtered_table = self._filter_single_file(tablefile, node_context)
            output_list.append(filtered_table)
