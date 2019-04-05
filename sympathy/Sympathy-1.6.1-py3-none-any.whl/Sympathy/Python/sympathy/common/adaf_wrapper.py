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
This module contains classes that wrap ADAFs or lists of ADAFs for use in
various function selector, F(x), nodes in Sympathy for Data.
"""
from sympathy.platform import exceptions as syexceptions
from sympathy.api import adaf  # NOQA
from . import fx_wrapper


class ADAFWrapper(fx_wrapper.FxWrapper):
    """
    ADAFWrapper should be used as the parent class for classes to be used
    in the ADAF F(x) nodes.
    """
    arg_types = ['adaf']
    list_wrapper = False

    def __init__(self, in_adaf, out_adaf, extra_table=None):
        self.required_signals = []
        self.in_adaf = in_adaf
        self.out_adaf = out_adaf
        self.extra_table = extra_table

    def execute(self):
        """Execute is called from the F(x) node."""
        raise syexceptions.SyConfigurationError(
            "This f(x) script doesn't implement an execute method.")


class ADAFsWrapper(ADAFWrapper):
    """ADAFsWrapper should be used as the parent class for classes to be used
    in the ADAFs F(x) nodes.

    Interact with the tables through in_table_list and out_table_list.
    """
    arg_types = ['[adaf]']
    list_wrapper = True

    def __init__(self, in_adaf, out_adaf, extra_table=None):
        super(ADAFsWrapper, self).__init__(in_adaf, out_adaf, extra_table)
        self.in_adaf_list = in_adaf
        self.out_adaf_list = out_adaf


class ADAFToTableWrapper(ADAFWrapper):
    """ADAFsToTablesWrapper should be used as the parent class for classes to
    be used in the ADAFs to Tables F(x) nodes.

    Interact with the files through in_adaf_list and out_table_list.
    """

    def __init__(self, in_adaf, out_table, extra_table=None):
        super(ADAFToTableWrapper, self).__init__(in_adaf, out_table,
                                                 extra_table)
        self.out_table = out_table


class ADAFsToTablesWrapper(ADAFToTableWrapper):
    """ADAFsToTablesWrapper should be used as the parent class for classes to
    be used in the ADAFs to Tables F(x) nodes.

    Interact with the files through in_adaf_list and out_table_list.
    """
    list_wrapper = True

    def __init__(self, in_adaf, out_table, extra_table=None):
        super(ADAFsToTablesWrapper, self).__init__(in_adaf, out_table,
                                                   extra_table)
        self.in_adaf_list = in_adaf
        self.out_table_list = out_table
