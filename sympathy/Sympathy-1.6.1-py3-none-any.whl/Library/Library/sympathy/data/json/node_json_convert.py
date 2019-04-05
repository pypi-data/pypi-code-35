# Copyright (c) 2019, System Engineering Software Society
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
from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api import exceptions
from sympathy.api import json


class JsonToDict(synode.Node):
    """
    Convert from JSON input containing a top-level dict to Sympathy
    dictionary (sydict) containing JSON.
    """

    author = 'Erik der Hagopian'
    icon = 'fromjson.svg'
    name = 'Json to Dict'
    nodeid = 'org.sysess.sympathy.json.jsontodict'
    tags = Tags(Tag.DataProcessing.Convert)

    inputs = Ports([Port.Json('JSON', name='json')])
    outputs = Ports([Port.Custom('{json}', 'JSON dict', name='json_dict')])

    def execute(self, node_context):
        data = node_context.input['json'].get()
        if not isinstance(data, dict):
            raise exceptions.SyDataError(
                'Conversion from json to {json} requires top-level dict')
        else:
            output = node_context.output['json_dict']
            for k, v in data.items():
                item = json.File()
                item.set(v)
                output[k] = item


class DictToJson(synode.Node):
    """
    Convert from Sympathy dictionary (sydict) input containing JSON to JSON
    dictionary.
    """

    author = 'Erik der Hagopian'
    icon = 'tojson.svg'
    name = 'Dict to Json'
    nodeid = 'org.sysess.sympathy.json.dicttojson'
    tags = Tags(Tag.DataProcessing.Convert)

    inputs = Ports([Port.Custom('{json}', 'JSON dict', name='json_dict')])
    outputs = Ports([Port.Json('JSON', name='json')])

    def execute(self, node_context):
        node_context.output['json'].set(
            {k: v.get() for k, v in node_context.input['json_dict'].items()})


class JsonToList(synode.Node):
    """
    Convert from Sympathy list (sylist) input containing JSON to JSON
    list.
    """

    author = 'Erik der Hagopian'
    icon = 'fromjson.svg'
    name = 'Json to List'
    nodeid = 'org.sysess.sympathy.json.jsontolist'
    tags = Tags(Tag.DataProcessing.Convert)

    inputs = Ports([Port.Json('JSON', name='json')])
    outputs = Ports([Port.Custom('[json]', 'JSON list', name='json_list')])

    def execute(self, node_context):
        data = node_context.input['json'].get()
        if not isinstance(data, list):
            raise exceptions.SyDataError(
                'Conversion from json to {json} requires top-level list')
        else:
            output = node_context.output['json_list']
            for v in data:
                item = json.File()
                item.set(v)
                output.append(item)


class ListToJson(synode.Node):
    """
    Convert from JSON input containing a top-level list to a Sympathy
    list (sylist) containing JSON.
    """

    author = 'Erik der Hagopian'
    icon = 'tojson.svg'
    name = 'List to Json'
    nodeid = 'org.sysess.sympathy.json.listtojson'
    tags = Tags(Tag.DataProcessing.Convert)

    inputs = Ports([Port.Custom('[json]', 'JSON list', name='json_list')])
    outputs = Ports([Port.Json('JSON', name='json')])

    def execute(self, node_context):
        node_context.output['json'].set(
            [v.get() for v in node_context.input['json_list']])
