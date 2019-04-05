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

import six
from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api import json


def remove_key(key, data, remove_all):
    """ Removes a key in a JSON structure """

    def walk_and_select(subdata, lookup_state):

        if isinstance(subdata, list):
            return [walk_and_select(item, lookup_state)
                    if isinstance(item, dict) else item for item in subdata]
        elif isinstance(subdata, dict):
            was_deleted = False
            if not lookup_state["removed"] or (lookup_state["removed"] and lookup_state["remove_all"]):
                try:
                    del subdata[lookup_state["key"]]
                    was_deleted = True
                    lookup_state["removed"] = True
                except KeyError:
                    pass
            if was_deleted and not remove_all:
                return subdata
            else:
                return {itemkey: (walk_and_select(item, lookup_state)
                                  if type(item) in [dict, list] else item)
                        for itemkey, item in six.iteritems(subdata)}
        else:
            return subdata

    return walk_and_select(data, lookup_state={"key": key, "remove_all": remove_all, "removed": False})


def select_key(key, data):
    """ Finds a key in a JSON structure """
    if isinstance(data, list):
        for item in data:
            lookup = select_key(key, item)
            if lookup:
                return lookup
    elif isinstance(data, dict):
        for itemkey, item in six.iteritems(data):
            if itemkey == key:
                return item
            else:
                lookup = select_key(key, item)
                if lookup:
                    return lookup
    else:
        if data == key:
            return data


def split_on_key(key, data):
    """ Split a JSON structure based on a key """
    if key == "<root>":
        if type(data) in [list, dict]:
            outjson = data
        else:
            return [data]
    else:
        selected = select_key(key, data)
        if selected:
            outjson = selected
        else:
            return [None]

    if isinstance(outjson, list):
        return [item for item in outjson]
    elif isinstance(outjson, dict):
        return [{key: item} for key, item in six.iteritems(outjson)]
    else:
        return [outjson]


class SuperNode(synode.Node):
    author = 'Samuel Genheden'
    version = '0.1'

    list_atomic_keys = False
    enable_root_select = False

    @staticmethod
    def parameters_base(**kwargs):
        parameters = synode.parameters()

        parameters.set_list(
            'key', label='JSON key',
            description='The key to select',
            **kwargs, editor=synode.Util.combo_editor())
        return parameters

    def adjust_parameters(self, node_context):
        keys = list()

        def enumerate_keys(subdata):
            """ Enumerate all keys that have a list or dictionary as item """
            if isinstance(subdata, list):
                for iitem in subdata:
                    enumerate_keys(iitem)
            elif isinstance(subdata, dict):
                for key, iitem in six.iteritems(subdata):
                    if type(iitem) in [dict, list] or self.list_atomic_keys:
                        keys.append(key)
                    enumerate_keys(iitem)

        if node_context.input[0].is_valid():

            if isinstance(node_context.input[0], json.File):
                jsons = node_context.input[0].get()
            else:
                jsons = [item.get() for item in node_context.input[0]]
            enumerate_keys(jsons)

        keys = list(sorted(set(keys)))
        if self.enable_root_select:
            keys.insert(0, "<root>")

        # Only update if we found a new list
        key_param = node_context.parameters['key']
        key_param.list = keys

    @staticmethod
    def execute_base(node_context, exec_func, **kwargs):

        def _make_new_file(data):
            jsonfile = json.File()
            jsonfile.set(data)
            return jsonfile

        key = node_context.parameters['key'].selected
        injson = node_context.input[0].get()
        outjson = exec_func(key, injson, **kwargs)

        if isinstance(node_context.output[0], json.File):
            node_context.output[0].set(outjson)
        else:
            node_context.output[0].extend([_make_new_file(item)
                                           for item in outjson])


class SelectKeyJson(SuperNode):
    """
    Select key in a JSON structure and from that create a new JSON

    Will only select the first occurrence of the key

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

    we can select the key ``"items"``, which will produce the new JSON

    .. code-block:: python

        {
            "a":"1",
            "b":"2",
            "c":"3"
        }

    """
    name = 'Select key JSON'
    icon = 'select_json_key.svg'
    tags = Tags(Tag.DataProcessing.Select)
    nodeid = 'org.sysess.sympathy.data.json.selectkeyjson'

    inputs = Ports([Port.Json('Input', name='input')])
    outputs = Ports([Port.Json('Output', name='output')])
    parameters = SuperNode.parameters_base()

    def execute(self, node_context):
        SuperNode.execute_base(node_context, select_key)


@node_helper.list_node_decorator(['input'], ['output'])
class SelectKeyJsons(SelectKeyJson):
    name = "Select key JSONs"
    nodeid = "org.sysess.sympathy.data.json.selectkeyjsons"


class RemoveKeyJson(SuperNode):
    """
    Remove a key from a JSON structure

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

    we can remove the keys ``"version"`` and ``"software"`` producing the new
    JSON

    .. code-block:: python

        {
           "items" : {
                "a":"1",
                "b":"2",
                 "c":"3"
            }
        }

    """
    name = 'Remove key JSON'
    icon = 'remove_json_key.svg'
    tags = Tags(Tag.DataProcessing.TransformStructure)
    nodeid = 'org.sysess.sympathy.data.json.removekeyjson'
    list_atomic_keys = True

    inputs = Ports([Port.Json('Input', name='input')])
    outputs = Ports([Port.Json('Output', name='output')])
    parameters = SuperNode.parameters_base()
    parameters.set_boolean("all", label='Remove all', value=False,
                           description="Remove all occurences of key, "
                           "not just first")

    def execute(self, node_context):
        remove_all = node_context.parameters['all'].value
        SuperNode.execute_base(node_context, remove_key, remove_all=remove_all)


@node_helper.list_node_decorator(['input'], ['output'])
class RemoveKeyJsons(RemoveKeyJson):
    name = "Remove key JSONs"
    nodeid = "org.sysess.sympathy.data.json.removekeyjsons"


class SplitOnKeyJson(SuperNode):
    """
    Select key in a JSON structure and split into multiple JSONs based on that
    key.
    Will only select the first occurrence of the key
    The special key ``<root>`` splits the JSON based on the root key

    For example the JSON:

    .. code-block:: python

        {
            "version":"1.0",
            "items" : [
                {
                    "a":"1",
                    "b":"2",
                    "c":"3"
                },
                {
                    "g":"1",
                    "h":"2",
                    "j":"3"
                }
            ]
        }

    can be splitted on the key ``"items"``, which will produce two new JSONs

    .. code-block:: python

        {
            "a":"1",
            "b":"2",
            "c":"3"
        }

    and

    .. code-block:: python

        {
            "g":"1",
            "h":"2",
            "j":"3"
        }

    """
    name = 'Split on key JSON'
    icon = 'split_json_key.svg'
    tags = Tags(Tag.DataProcessing.TransformStructure)
    description = 'Split a JSON structure into multiple JSONs'
    nodeid = 'org.sysess.sympathy.data.json.splitonkeyjson'

    inputs = Ports([Port.Json('Input', name='input')])
    outputs = Ports([Port.Jsons('Output', name='output')])
    parameters = SuperNode.parameters_base(value_names=['<root>'])
    enable_root_select = True

    def execute(self, node_context):
        SuperNode.execute_base(node_context, split_on_key)


@node_helper.list_node_decorator(['input'], ['output'])
class SplitOnKeyJsons(SplitOnKeyJson):
    name = "Split on key JSONs"
    nodeid = "org.sysess.sympathy.data.json.splitonkeyjsons"
