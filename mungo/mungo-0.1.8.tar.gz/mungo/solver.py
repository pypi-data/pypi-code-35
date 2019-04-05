import re

from collections import defaultdict
from functools import partial, reduce
from pulp import *
from functools import lru_cache

from packaging.version import parse as _vparse


def vparse(v, end=""):
    # print(v, _vparse(v.strip("*").strip(".")))
    return _vparse(v.strip("*").strip(".") + end)


operator_function = {
    ">=": lambda x, y: vparse(x) >= vparse(y),
    ">": lambda x, y: vparse(x) > vparse(y),
    "<=": lambda x, y: vparse(x) <= vparse(y),
    "<": lambda x, y: vparse(x) < vparse(y),
    "!=": lambda x, y: vparse(x) != vparse(y),
    "=": lambda x, y: (vparse(x) >= vparse(y)) and (vparse(x) < vparse(y, ".99999999999999")),
    "==": lambda x, y: (vparse(x) >= vparse(y)) and (vparse(x) < vparse(y, ".99999999999999")),
}


class Node:
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
        self.invalid = False

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
        if self.p is None or "channel" not in self.p:
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


@lru_cache()
def valid_packages(ls, repodata):
    all_valids = []
    for s in ls:
        name, is_valid = _valid_packages_function(s)
        all_valids.append(is_valid)

    # all_valid = lambda x: reduce((lambda a, b: a(x) and b(x)), all_valids)
    all_valid = lambda x: all([f(x) for f in all_valids])

    return [(name, v) for v in repodata.d[name] if all_valid(v)]


def split_package_constraint(s):
    split = s.split(",")
    ret = []

    for i, x in enumerate(split):
        res = re.split('(==|!=|>=|<=|=|<|>| )', x)
        res = [y for y in res if y != " " and len(y) > 0]
        if i == 0:
            name = res.pop(0)
        ret.append(res)

    return name, ret


def _valid_packages_function(s):
    name, constraints = split_package_constraint(s)

    is_valids = []  # lambda x: True

    for c in constraints:
        len_c = len(c)
        if len_c == 0:
            # no version constraint
            pass
        elif len_c == 1:
            # version constraint without operator (equals ==)
            version = c[0]
            is_valids.append(lambda x: partial(operator_function["="], y=version)(x))
        elif len_c == 2:
            # version constraint
            operator, version = c
            if operator in [">=", ">", "<=", "<", "!=", "=", "=="]:
                is_valids.append(lambda x: partial(operator_function[operator], y=version)(x))
            else:
                # version build constraint with no operator
                # TODO: dont ignore build
                version, build = c
                is_valids.append(lambda x: partial(operator_function["="], y=version)(x))
        else:
            raise Exception("invalid version constraint", s)

    is_valid = lambda x: all([f(x) for f in is_valids])
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

    # multiple constraints may refer the same package
    # group them

    grouped_dependencies = defaultdict(list)
    for dependency in dependencies:
        name = split_package_constraint(dependency)[0]
        grouped_dependencies[name].append(dependency)

    # print("openssl 1.0.1", list(valid_packages(["openssl 1.0.1"], repodata)))
    # exit()

    # print(name, version, grouped_dependencies)
    for dependency in grouped_dependencies.values():
        d_node = None
        # make sure s is list like if string
        if isinstance(dependency, str):
            dependency = (dependency,)
        for d_name, d_version in valid_packages(tuple(dependency), repodata):
            d_node = create_node(d_name, d_version, repodata, new_node, all_nodes)
            new_node.add_out_node(d_node)

        if d_node is None:  # no versions were found for a dependency
            print("Warning:", "no packages found for", *dependency)
            new_node.invalid = True
            # raise Exception("no packages found for", *dependency)

    return new_node


def reduce_dag(all_nodes, channels):
    # reduce DAG

    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

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
