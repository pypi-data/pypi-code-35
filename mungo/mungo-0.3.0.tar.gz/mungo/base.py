import sys

from collections import defaultdict
from subprocess import run

from conda.models.version import VersionOrder

from pulp import *
from yaml import safe_load

from mungo.repodata import Repodata, merge_repodata, get_repository_data
from mungo.solver import create_node, reduce_dag
from mungo.cli import print_dag, _install_prompt


def vparse(v, add=""):
    version, build = v
    version = version.strip("*").strip(".")
    # print(v, _vparse(v.strip("*").strip(".")))
    return VersionOrder(f"{version}{add}"), f"{build}"


def create_dag(channels, packages, local_repodata, njobs=8, offline=False, force_download=False):
    repodata_chunks = get_repository_data(channels, njobs, offline, force_download)
    repodata = merge_repodata(local_repodata + repodata_chunks)

    # add installed packages to the repodata

    # default_packages = {"sqlite", "wheel", "pip"}
    default_packages = set()

    all_nodes = defaultdict(dict)
    root = create_node("root", ("0", "0"), repodata, all_nodes=all_nodes,
                       override_dependencies=list(packages | default_packages))

    # reduce DAG
    reduce_dag(all_nodes, channels)
    return all_nodes, root


def nodes_to_install(all_nodes, root, channels):
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

    # create ILP problem
    prob = LpProblem("DependencySolve", LpMinimize)

    # build LP on the reduced DAG
    objective = []
    prob += root.x == 1

    # n.p['channel'].split('/')[-2]

    # create brother information
    for name, versions in all_nodes.items():
        big_brother = None
        # small hack to make local always be the highest

        for v in sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name] + versions[v].is_installed * (priority + 1), vparse(v)), reverse=True):
            n = versions[v]
            n.big_brother = big_brother
            big_brother = n

    def mass(n):
        if n is None:
            return 0, 0

        if n._mass_low is None:
            n._mass_low = 0  # temporarily set mass to 0 for loops in "DAG"
            n._mass_high = 0  # temporarily set mass to 0 for loops in "DAG"
            m_low = 0
            m_high = 0
            for children in n._out_nodes.values():
                children_masses = [mass(c) for c in children]
                m_low += min([c for c, _ in children_masses])
                m_high += max([c for _, c in children_masses])
            # n._mass_low = m_low + 1 + mass(n.big_brother)[1]
            # n._mass_high = m_high + 1 + mass(n.big_brother)[1]
            n._mass_high = m_high - m_low + 1 + mass(n.big_brother)[1]
            n._mass_low = 1 + mass(n.big_brother)[1]
        return n._mass_low, n._mass_high

    # for name, versions in all_nodes.items():
    #     for version, n in versions.items():
    #         print(name, version, mass(n))

    for name, versions in all_nodes.items():
        # constraint: install at most one version of a package
        prob += sum(n.x for n in versions.values()) <= 1
        # exclude invalid node
        # constraint: if a parent is installed, one version of each dependency must be installed too
        for current_node in versions.values():
            if current_node.invalid: # exlude invalid nodes
                prob += current_node.x == 0
                break

            for out_group in current_node._out_nodes.values():
                prob += sum([n.x for n in out_group]) >= current_node.x

        # for n in versions.values():
        #     print(n.factor, n.normalized_version, n.name, n.version)

        # storing the objectives
        objective.extend([mass(n)[0] * n.x for n in versions.values()])
        # print([(n.name, n.normalized_version, n.factor) for n in versions.values()])

        if current_node is root:  # no no_install for root  # FIXME current_node might be uninitialized
            continue

    prob += sum(objective)
    prob.writeLP("WhiskasModel.lp")
    prob.solve()

    if prob.status != LpStatusOptimal:
        print(f"ERROR: Solution is not optimal (status: {LpStatus[prob.status]}).\nAborting.", file=sys.stderr)
        exit(1)

    # for v in prob.variables():
    #     print(v.name, v.varValue)

    # collect all install nodes
    install_nodes = []
    for _, versions in sorted(all_nodes.items()):
        for n in versions.values():
            if n.p is None:  # skip root
                continue
            x = n.x
            if x.varValue == 1.0:
                install_nodes.append(n)

    return sorted(install_nodes, key=lambda x: x.factor)


def read_environment_description(yml):
    with open(yml, 'rt') as reader:
        data = safe_load(reader)
        name = data.get('name', None)
        channels = data.get('channels', [])
        package_specs = {p for p in data.get('dependencies', []) if isinstance(p, str)}
        pip_specs = [p['pip'] for p in data.get('dependencies', []) if isinstance(p, dict) and 'pip' in p]
        pip_specs = {item for sublist in pip_specs for item in sublist}
        return name, channels, package_specs, pip_specs


def _get_condarc_channels():
    with open(os.path.expanduser(os.path.join('~', '.condarc')), 'rt') as reader:
        channels = safe_load(reader)
        return channels['channels']

def create_environment(name, channels, packages, pip, jobs=1, dag=False, ask_for_confirmation=False, offline=False, force_download=False):
    all_nodes, root = create_dag(channels, packages, [], jobs, offline, force_download)
    to_install = nodes_to_install(all_nodes, root, channels)
    if dag:
        print_dag(all_nodes, root, to_install)
    else:
        if _install_prompt(to_install, None, ask_for_confirmation):
            command = "@EXPLICIT\n"
            command += '\n'.join([f'{n.p["channel"]}/{n.p["fn"]}' for n in to_install])
            ps = run(f'bash -i -c "conda create --name {name} --file /dev/stdin"', input=command.encode(), shell=True)


def install_packages(name, channels, packages, pip, jobs=1, dag=False, ask_for_confirmation=False, offline=False, force_download=False):
    local_repodata = Repodata.from_environment(name)
    all_nodes, root = create_dag(channels, packages, [local_repodata], jobs, offline, force_download)
    to_install = nodes_to_install(all_nodes, root, channels)
    if dag:
        print_dag(all_nodes, root, to_install)
    else:
        to_install = [n for n in to_install if "installed" not in n.p]
        installed = local_repodata.d
        if _install_prompt(to_install, installed, ask_for_confirmation):
            command = "@EXPLICIT\n"
            command += '\n'.join([f'{n.p["channel"]}/{n.p["fn"]}' for n in to_install])
            ps = run('bash -i -c "conda install --file /dev/stdin"', input=command.encode(), shell=True)
