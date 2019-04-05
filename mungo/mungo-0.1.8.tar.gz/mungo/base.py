from collections import defaultdict
from subprocess import run

from graphviz import Digraph
from packaging.version import parse as vparse
from pulp import *
from yaml import safe_load

from mungo.repodata import Repodata, merge_repodata, get_repository_data
from mungo.solver import create_node, reduce_dag


def create_dag(channels, packages, local_repodata, njobs=4):
    repodata_chunks = get_repository_data(channels, njobs)
    repodata = merge_repodata(local_repodata + repodata_chunks)

    # add installed packages to the repodata

    # default_packages = {"sqlite", "wheel", "pip"}
    default_packages = set()

    all_nodes = defaultdict(dict)
    root = create_node("root", "", repodata, all_nodes=all_nodes,
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
        for v in sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name], vparse(v)),
                        reverse=True):
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
            if x.varValue == 1.0 and not x.name.endswith("_no_install"):
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


def print_dag(all_nodes, root):
    dot = Digraph()
    # nodes
    for n in all_nodes.values():
        for v in n.values():
            dot.node(f"{v.name}_{v.version}", f"{v.name} {v.version}")

    # edges
    for n in all_nodes.values():
        for v in n.values():
            for o in v.out_nodes:
                dot.edge(f"{v.name}_{v.version}", f"{o.name}_{o.version}")

    print(dot.source)


def create_environment(name, channels, packages, pip, jobs=1, dag=False, ask_for_confirmation=False):
    all_nodes, root = create_dag(channels, packages, [], jobs)
    if dag:
        print_dag(all_nodes, root)
    else:
        to_install = nodes_to_install(all_nodes, root, channels)
        if _install_prompt(to_install, None, ask_for_confirmation):
            command = "@EXPLICIT\n"
            command += '\n'.join([f'{n.p["channel"]}/{n.p["fn"]}' for n in to_install])
            ps = run(f'bash -i -c "conda create --name {name} --file /dev/stdin"', input=command.encode(), shell=True)


def install_packages(name, channels, packages, pip, jobs=1, dag=False, ask_for_confirmation=False):
    local_repodata = Repodata.from_environment(name)
    all_nodes, root = create_dag(channels, packages, [local_repodata], jobs)
    if dag:
        print_dag(all_nodes, root)
    else:
        to_install = [n for n in nodes_to_install(all_nodes, root, channels) if "installed" not in n.p]
        installed = local_repodata.d
        if _install_prompt(to_install, installed, ask_for_confirmation):
            command = "@EXPLICIT\n"
            command += '\n'.join([f'{n.p["channel"]}/{n.p["fn"]}' for n in to_install])
            ps = run('bash -i -c "conda install --file /dev/stdin"', input=command.encode(), shell=True)


def _install_prompt(to_install, installed=None, ask_for_confirmation=True):
    if len(to_install) == 0:
        print("Nothing to do.")
        exit(0)

    def _prepare_packages(packages):
        # update package information to contain everything we need for displaying relevant information
        for package, ds in packages.items():
            for data in ds:
                if data is not None:
                    data['version_build'] = data['version'] + '-' + data['build']
                    if "channel" not in data:
                        data['reponame'] = "local" # TODO: replace this
                    else:
                        data['reponame'] = data['channel'].split('/')[-2]
        return packages

    def _calculate_widths(packages):
        # calculate column-widths for the three columns 'name', 'version_build' and 'reponame'
        widths = {t: max([max([len(d_from[t]) if d_from is not None else 0, len(d_to[t])])
                          for (d_from, d_to) in packages.values()]) if len(packages) > 0 else 0
                  for t in ['name', 'version_build', 'reponame']}
        return widths

    def _print_packages(packages, widths):
        # print packages that are to be installed / updated / downgraded
        print("")
        for (package_from, package_to) in sorted(packages.values(),
                                                 key=lambda x: x[1]['factor'] if x[1] is not None else 0):
            if "installed" not in package_to:  # only display packages that aren't already installed
                if package_from is not None:  # if there's an update/downgrade of a package
                    print("\t{:<{name_width}} {:<{version_width}} {:<{repo_width}}  ->  "
                          "{:<{version_width}} {:<{repo_width}}"
                          .format(package_from['name'], package_from['version_build'], package_from['reponame'],
                                  package_to['version_build'], package_to['reponame'],
                                  name_width=widths['name'],
                                  version_width=widths['version_build'],
                                  repo_width=widths['reponame']))
                else:  # install a new package (not an update/downgrade of an existing package)
                    print("\t{:<{name_width}} {:<{version_width}} {:<{repo_width}}"
                          .format(package_to['name'], package_to['version_build'], package_to['reponame'],
                                  name_width=widths['name'],
                                  version_width=widths['version_build'],
                                  repo_width=widths['reponame']))
        print("")

    for node in to_install:
        # embellish the data of the node with the node's factor (which is used for sorting)
        node.p['factor'] = node.factor
    to_install = {node.p['name']: node.p for node in to_install}

    if installed is not None:
        # which packages have changed?
        changed = installed.keys() & to_install.keys()

        # assert that there is only one version installed.
        # TODO: What do we do if there are multiple versions?
        if not all(len(installed[package].keys()) == 1 for package in installed.keys()):
            print(f"Warning: Multiple locally installed versions for the same package.")

        local_versions = {name: list(installed[name].values())[0] for name in changed}
        remote_versions = {name: data for name, data in to_install.items() if name in changed}
        version_changes = {package: (local_versions[package], remote_versions[package]) for package in changed}

        upgrades = {package: (p_from, p_to)
                    for (package, (p_from, p_to)) in version_changes.items()
                    if vparse('-'.join([p_from['version'], p_from['build']]))
                    < vparse('-'.join([p_to['version'], p_to['build']]))}
        downgrades = {package: (p_from, p_to)
                      for (package, (p_from, p_to)) in version_changes.items()
                      if vparse('-'.join([p_from['version'], p_from['build']]))
                      > vparse('-'.join([p_to['version'], p_to['build']]))}

        # remove packages that are to be updated or downgraded from the list of *new* packages
        for package in upgrades.keys() | downgrades.keys():
            to_install.pop(package, None)
    else:
        upgrades = dict()
        downgrades = dict()

    # add a dummy "package_from" (`None`) to get rid of special cases
    to_install = {package: (None, p_to) for (package, p_to) in to_install.items()}

    # get maximum column widths per type
    # across all three modes of package installation (install/upgrade/downgrade)
    all_widths = [_calculate_widths(_prepare_packages(packages)) for packages in [to_install, upgrades, downgrades]]
    widths = dict()
    for w in all_widths:
        for k, v in w.items():
            widths[k] = max(widths.get(k, 0), v)

    if len(upgrades) > 0:
        print("The following packages will be UPDATED:")
        _print_packages(upgrades, widths)

    if len(downgrades) > 0:
        print("The following packages will be DOWNGRADED:")
        _print_packages(downgrades, widths)

    if len(to_install) > 0:
        print("The following packages will be INSTALLED:")
        _print_packages(to_install, widths)

    if ask_for_confirmation:
        answer = input("\nProceed ([y]/n)? ")
        if answer.lower() not in {'\n', 'y'}:
            return False
    return True
