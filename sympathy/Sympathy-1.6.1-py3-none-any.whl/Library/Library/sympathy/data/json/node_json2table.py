# -*- coding: utf-8 -*-
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

from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sylib.json_table import (JsonTableWidget, JsonTable,
                              add_jsontable_parameters, TABLE_KIND)


def parameters_base():
    parameters = synode.parameters()
    add_jsontable_parameters(parameters)
    return parameters


class JsonToTable(synode.Node):
    """
    Convert a JSON file to a Table

    There are two kinds of tables that can be created:

        * Single row – where the JSON structure is simply flattened
        * Multiple rows - where the JSON structure is recursively expanded to
          create several rows

    If a single-row table is created, there is an option to minimize the
    column names to remove unnecessary path information from the JSON keys.

    For example from the JSON:

    .. code-block:: python

        {
            "version":"1.0",
            "software":"sfd",
            "items" : {
                "a":"1",
                "b":"2",
                 "c":"3"
            }
        }

    we can create the following single-row table

    .. code-block:: python

        version    software    items.a    items.b    items.c
        ----------------------------------------------------
        1.0        sfd         1          2          3

    and the column names can be *minimized* to

     .. code-block:: python

        version    software    a    b    c
        -------------------------------------
        1.0        sfd         1    2    3


    If a multiple rows-table is created, the recursive algorithm might identify
    keys and therefore columns that are lacking some values. One can choose to
    fill in the missing values with a **empty string**, a **nan** string or
    **mask** the value.

    For example from the JSON:

    .. code-block:: python

        {
            "version":"1.0",
            "software":"sfd",
            "items" : [
                {
                    "a":"1",
                    "b":"2",
                    "c":"3"
                },
                {
                    "a":"67",
                    "b":"77",
                    "d":"97"
                }
            ]
        }

    we can create the following multiple-rows table

    .. code-block:: python

        version    software    a    b    c    d
        -------------------------------------------
        1.0        sfd         1    2    3    ---
        1.0        sfd         67   77   ---  97

    where the ``c`` column is masked in the second row and the ``d``
    column is masked in the first row.

    If the algorithm that creates tnhe multi-row table fails to produce
    the desired table, it might be worth using other nodes to remove,
    select or split the JSON structure on some key.
    """
    name = 'JSON to Table'
    author = 'Samuel Genheden'
    version = '0.1'
    icon = 'json2table.svg'
    tags = Tags(Tag.DataProcessing.Convert)
    nodeid = 'org.sysess.sympathy.data.json.jsontotable'

    inputs = Ports([Port.Json('Input JSON object', name='input')])
    outputs = Ports([Port.Table('Output table', name='output')])
    parameters = parameters_base()

    def exec_parameter_view(self, node_context):
        return JsonTableWidget(node_context.parameters)

    def execute(self, node_context):
        table_kind = node_context.parameters['table_kind'].value
        min_col_names = node_context.parameters['minimize_col_names'].value
        nomask = node_context.parameters['nomask'].value

        tbl = JsonTable(node_context.input[0])
        if table_kind == TABLE_KIND["SINGLE"]:
            node_context.output[0].source(
                tbl.create_single_row_table(min_col_names))
        else:
            node_context.output[0].source(
                tbl.create_multiple_rows_table(nomask))


@node_helper.list_node_decorator(['input'], ['output'])
class JsonsToTables(JsonToTable):
    name = "JSONs to Tables"
    nodeid = "org.sysess.sympathy.data.json.jsonstotables"
