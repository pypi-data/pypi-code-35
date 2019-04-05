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
from sympathy.api.nodeconfig import (Port, Ports, Tag, Tags)
from sympathy.api.exceptions import SyNodeError
import sylib.error


class InsertItemDict(synode.Node):
    """
    Create a dict with the items from dict (input) but with item inserted.

    If the key already exists it will be replaced.
    """
    author = 'Erik der Hagopian'
    description = 'Insert item in dict'
    icon = 'insert_item_dict.svg'
    name = 'Insert Dict'
    nodeid = 'org.sysess.sympathy.dict.insert'
    tags = Tags(Tag.Generic.Dict)

    parameters = synode.parameters()
    parameters.set_string('key', label='Key', value='')

    inputs = Ports([
        Port.Custom('{<a>}', 'Dict', name='dict'),
        Port.Custom('<a>', 'Item', name='item')])
    outputs = Ports([
        Port.Custom('{<a>}', 'Dict', name='dict')])

    def verify_parameters(self, node_context):
        key = node_context.parameters['key'].value
        return True if key else False

    def execute(self, node_context):
        key = node_context.parameters['key'].value
        item = node_context.input['item']
        input_dict = node_context.input['dict']
        output_dict = node_context.output['dict']

        if key:
            tmp_dict = dict(input_dict.items())
            tmp_dict[key] = item

            output_dict.update(tmp_dict)


class UpdateDict(synode.Node):
    """
    Create a dict with the items from dicts (input).
    If there are duplicate keys they will be replaced.
    """
    author = 'Erik der Hagopian'
    description = 'Update dict with input from dict(s)'
    icon = 'dicts_to_dict.svg'
    name = 'Update Dict'
    nodeid = 'org.sysess.sympathy.dict.update'
    tags = Tags(Tag.Generic.Dict)

    inputs = Ports([
        Port.Custom('{<a>}', 'Dict', name='dict', n=(2,))])
    outputs = Ports([
        Port.Custom('{<a>}', 'Dict', name='dict')])

    def execute(self, node_context):
        output_dict = node_context.output['dict']
        tmp_dict = {}
        for dict_ in node_context.input.group('dict'):
            tmp_dict.update(dict_.items())

        output_dict.update(tmp_dict)


_basic_error_strategy = sylib.error.strategy('basic')


class GetItemDict(synode.Node):
    """Get one item in dict by key."""

    author = 'Erik der Hagopian'
    description = 'Get one item in dict by key'
    icon = 'dict_to_item.svg'
    name = 'Get Item Dict'
    nodeid = "org.sysess.sympathy.dict.getitem"
    tags = Tags(Tag.Generic.Dict)

    inputs = Ports(
        [Port.Custom('{<a>}', 'Dict', name='dict'),
         Port.Custom('<a>', 'Default item', name='default',
                     n=(0, 1, 0))])
    outputs = Ports(
        [Port.Custom('<a>', 'Item', name='item')])

    parameters = synode.parameters()
    parameters.set_string(
        'key', label='Key', value='',
        description='Choose item key in dict.',
        editor=synode.Util.combo_editor(include_empty=True, edit=True))

    parameters.set_string(
        'fail_strategy', label='Action on missing key',
        value='error',
        description='Decide how a missing key should be handled',
        editor=synode.Util.combo_editor(options=_basic_error_strategy.options))

    def adjust_parameters(self, node_context):
        keys = []
        input_dict = node_context.input['dict']
        if input_dict.is_valid():
            keys = input_dict.keys()
        node_context.parameters['key'].adjust(keys)

    def verify_parameters(self, node_context):
        key = node_context.parameters['key'].value
        return True if key else False

    def execute(self, node_context):
        input_dict = node_context.input['dict']
        key = node_context.parameters['key'].value

        if key in input_dict:
            node_context.output['item'].source(
                input_dict[key], shallow=True)
        else:
            defaults = node_context.input.group('default')
            if defaults:
                node_context.output['item'].source(defaults[0])
            elif _basic_error_strategy.is_error(
                    node_context.parameters['fail_strategy'].value):
                raise SyNodeError('Key: "{}" is not in dict.'.format(key))


class ItemsToDict(synode.Node):
    """
    Create a multi item dict containing items.
    Items without name are ignored.
    """
    author = 'Erik der Hagopian'
    icon = 'list_to_dict.svg'
    name = 'Items to Dict'
    nodeid = "org.sysess.sympathy.dict.fromitems"
    tags = Tags(Tag.Generic.Dict)

    inputs = Ports(
        [Port.Custom('[(text, <a>)]', 'List', name='list')])
    outputs = Ports(
        [Port.Custom('{<a>}', 'Dict', name='dict')])

    def execute(self, node_context):
        input_list = node_context.input['list']
        output_dict = node_context.output['dict']
        tmp_dict = {}
        for item in input_list:
            name = item[0].get()
            if name:
                tmp_dict[name] = item[1]

        output_dict.update(tmp_dict)


class DictValues(synode.Node):
    """
    Create a list of items from dict, sorted by key.
    """
    author = 'Erik der Hagopian'
    icon = 'dict_to_list.svg'
    name = 'Dict values'
    nodeid = "org.sysess.sympathy.dict.values"
    tags = Tags(Tag.Generic.Dict)

    inputs = Ports(
        [Port.Custom('{<a>}', 'Dict', name='dict')])
    outputs = Ports(
        [Port.Custom('[<a>]', 'List', name='list')])

    def execute(self, node_context):
        input_dict = node_context.input['dict']
        output_list = node_context.output['list']

        for _, item in sorted(input_dict.items(), key=lambda x: x[0]):
            output_list.append(item)


class DictKeys(synode.Node):
    """
    Create a list of keys from dict, sorted by key.
    """
    author = 'Erik der Hagopian'
    icon = 'dict_to_list.svg'
    name = 'Dict keys'
    nodeid = "org.sysess.sympathy.dict.keys"
    tags = Tags(Tag.Generic.Dict)

    inputs = Ports(
        [Port.Custom('{<a>}', 'Dict', name='dict')])
    outputs = Ports(
        [Port.Custom('[text]', 'List', name='list')])

    def execute(self, node_context):
        input_dict = node_context.input['dict']
        output_list = node_context.output['list']

        for key, _ in sorted(input_dict.items(), key=lambda x: x[0]):
            output_item = output_list.create()
            output_item.set(key)
            output_list.append(output_item)


class DictItems(synode.Node):
    """
    Create a list of tuples (key, value) from dict, sorted by key.
    """
    author = 'Erik der Hagopian'
    icon = 'dict_to_list.svg'
    name = 'Dict items'
    nodeid = "org.sysess.sympathy.dict.items"
    tags = Tags(Tag.Generic.Dict)

    inputs = Ports(
        [Port.Custom('{<a>}', 'Dict', name='dict')])
    outputs = Ports(
        [Port.Custom('[(text, <a>)]', 'List', name='list')])

    def execute(self, node_context):
        input_dict = node_context.input['dict']
        output_list = node_context.output['list']

        for key, value in sorted(input_dict.items(), key=lambda x: x[0]):
            output_item = output_list.create()
            output_item[0].set(key)
            output_item[1].source(value, shallow=True)
            output_list.append(output_item)
