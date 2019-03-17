# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG HanYang PUA conversion table reader
#   Copyright (C) 2015-2019 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function

from .models import Node


def build_tree(mappings):
    root = Node(
        parent=-1,
        source=None,
        target=None,
    )
    nodelist = [root]
    node_childrens = [{}]
    for mapping in mappings:

        node_index = 0
        node = nodelist[node_index]
        node_children = node_childrens[node_index]

        source_codepoints = mapping.source
        target_codepoint = mapping.target
        for source_codepoint in source_codepoints:
            if source_codepoint in node_children:
                node_index = node_children[source_codepoint]
                node = nodelist[node_index]
                node_children = node_childrens[node_index]
            else:
                parent = node_index
                node_index = len(nodelist)
                node = Node(
                    parent=parent,
                    source=source_codepoint,
                    target=None,
                )
                nodelist.append(node)
                node_children[source_codepoint] = node_index
                node_children = {}
                node_childrens.append(node_children)
        nodelist[node_index] = node._replace(target=target_codepoint)

    node_childrens = [
        tuple(sorted(children.items()))
        for children in node_childrens
    ]
    return (
        tuple(nodelist),
        tuple(node_childrens),
    )


def build_tree_children_list(nodelist):
    node_childrens = [{} for node in nodelist]
    for node_index, node in enumerate(nodelist):
        if node.parent < 0:
            continue
        parent_children = node_childrens[node.parent]
        parent_children[node.source] = node_index
    node_childrens = [
        tuple(sorted(children.items()))
        for children in node_childrens
    ]
    return tuple(node_childrens)
