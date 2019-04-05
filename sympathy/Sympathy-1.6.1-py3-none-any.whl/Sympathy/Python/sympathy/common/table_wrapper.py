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
"""
This module contains classes that wrap tables or lists of tables for use in
various function selector, F(x), nodes in Sympathy for Data.
"""
from sympathy.platform import exceptions as syexceptions
from sympathy.api import table  # NOQA
from . import fx_wrapper


class TableWrapper(fx_wrapper.FxWrapper):
    """
    TableWrapper should be used as the parent class for classes to be used
    in the table F(x) nodes.

    Interact with the table through in_table and out_table.
    """
    arg_types = ['table']
    list_wrapper = False

    def __init__(self, in_table, out_table, extra_table=None):
        self.in_table = in_table
        self.out_table = out_table
        self.extra_table = extra_table

    def execute(self):
        """Execute is called from the F(x) node."""
        raise syexceptions.SyConfigurationError(
            "This f(x) script doesn't implement an execute method.")


class TablesWrapper(TableWrapper):
    """TablesWrapper should be used as the parent class for classes to be used
    in the tables F(x) nodes.

    Interact with the tables through in_table_list and out_table_list.
    """
    arg_types = ['[table]']
    list_wrapper = True

    def __init__(self, in_table, out_table, extra_table=None):
        super(TablesWrapper, self).__init__(in_table, out_table, extra_table)
        self.in_table_list = in_table
        self.out_table_list = out_table
