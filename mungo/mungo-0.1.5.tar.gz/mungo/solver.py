import re

from collections import defaultdict
from functools import partial, reduce
from pulp import *

from packaging.version import parse as vparse

operator_function = dict()
operator_function[">="] = lambda x, y: x >= y
operator_function[">"] = lambda x, y: x > y
operator_function["<="] = lambda x, y: x <= y
operator_function["<"] = lambda x, y: x < y
operator_function["!="] = lambda x, y: x != y
operator_function["="] = lambda x, y: x == y
operator_function["=="] = lambda x, y: x == y


class Node():
    def __init__(self, name, version, p):
        self.name = name
        self.version = version
        self.factor = 1
        self._in_nodes = []
        self._out_nodes = defaultdict(list)
        self._x = None
        self.p = p
        self._mass_low = None
        self._mass_high = None

    def delete(self):
        for n in self.in_nodes:
            n.out_nodes.remove(self.current_node)
        for n in self.out_nodes:
            n.in_nodes.remove(self.current_node)

    def add_in_node(self, n):
        self._in_nodes.append(n)

    def remove_in_node(self, n):
        self._in_nodes.remove(n)

    def add_out_node(self, n):
        self._out_nodes[n.name].append(n)

    def remove_out_node(self, n):
        self._out_nodes[n.name].remove(n)

    @property
    def channel_name(self):
        if self.p is None:
            return ""
        return self.p['channel'].split('/')[-2]

    @property
    def in_nodes(self):
        return self._in_nodes

    @property
    def out_nodes(self):
        for nodes in self._out_nodes.values():
            for n in nodes:
                yield n

    @property
    def x(self):
        # create LP variable, if not exist
        if self._x is None:
            self._x = LpVariable("{name}-{version}".format(name=self.name, version=self.version), 0, 1, LpInteger)
        return self._x

    def delete(self):
        for n in self.in_nodes:
            n.remove_out_node(self)
        for n in self.out_nodes:
            n.remove_in_node(self)


def valid_packages(ls, repodata):
    # make sure s is list like if string
    if isinstance(ls, str):
        ls = [ls]

    all_valids = []
    for s in ls:
        name, is_valid = _valid_packages_function(s)
        all_valids.append(is_valid)

    all_valid = lambda x: reduce((lambda a, b: a(x) and b(x)), all_valids)

    for v in repodata.d[name]:
        if all_valid(v):
            yield (name, v)


def split_package_constain(s):
    split = re.split('(==|!=|>=|<=|=|<|>| )', s)
    return [s for s in split if not s == " " and len(s)]


def _valid_packages_function(s):
    split = split_package_constain(s)

    if len(split) == 5:
        name, operator1, version1, operator2, version2 = split
        is_valid = lambda x: partial(operator_function[operator1], y=vparse(version1))(vparse(x)) and partial(
            operator_function[operator2], y=vparse(version2))(vparse(x))
    elif len(split) == 3:
        # version constraint
        name, operator, version = split
        if operator in [">=", ">", "<=", "<", "!=", "=", "=="]:
            is_valid = lambda x: partial(operator_function[operator], y=vparse(version))(vparse(x))
        else:
            # version build constraint
            name, version, build = split
            is_valid = lambda x: partial(operator_function["="], y=vparse(version))(vparse(x))
    elif len(split) == 2:
        # version constraint without operator (equals ==)
        name, version = split
        is_valid = lambda x: partial(operator_function["="], y=vparse(version))(vparse(x))
    elif len(split) == 1:
        # no version constraint
        name, = split
        is_valid = lambda x: True
    else:
        raise Exception("invalid version constraint", s)

    return name, is_valid


def create_node(name, version, repodata,
                sender=None,
                all_nodes=defaultdict(dict),
                override_dependencies=None):
    if version in all_nodes[name]:
        node = all_nodes[name][version]
        node.add_in_node(sender)  # add the parent to in-nodes
        return node

    # create new node
    if version in repodata.d[name]:
        p = repodata.d[name][version]
    else:
        p = None

    new_node = Node(name, version, p)

    if sender is not None:
        new_node.add_in_node(sender)

    all_nodes[name][version] = new_node

    # get package information from repodata
    if override_dependencies is not None:
        dependencies = override_dependencies
    else:
        dependencies = p["depends"]


    # multiple constrains may refer the same package
    # group them

    grouped_dependencies = defaultdict(list)
    for dependency in dependencies:
        name = split_package_constain(dependency)[0]
        grouped_dependencies[name].append(dependency)

    for dependency in grouped_dependencies.values():
        d_node = None
        for d_name, d_version in valid_packages(dependency, repodata):
            d_node = create_node(d_name, d_version, repodata, new_node, all_nodes)
            new_node.add_out_node(d_node)

        if d_node is None: # no versions were found
            raise Exception("no packages found for", *dependency)
    return new_node


def reduce_dag(all_nodes, channels):
    # reduce DAG

    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel=="defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1 # highest priority for local installed packages

    for name, versions in all_nodes.items():
        seen_keys = set()
        for v in sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name], vparse(v)), reverse=True):
            current_node = versions[v]
            in_node_key = tuple(sorted([(n.name, n.version) for n in current_node.in_nodes]))
            out_node_key = tuple(sorted([(n.name, n.version) for n in current_node.out_nodes]))
            key = (in_node_key, out_node_key)
            if key in seen_keys:
                # the in-node out-node combination exist in a higher version of the same package
                # thus the higher version is ALWAYS preferable and this version can be removed
                current_node.delete()
                del (all_nodes[name][v])
            else:
                seen_keys.add(key)
