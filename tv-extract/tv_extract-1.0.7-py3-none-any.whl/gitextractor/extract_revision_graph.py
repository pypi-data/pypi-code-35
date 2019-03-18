import logging
import os

from typing import Dict
from tv_extract.gitextractor.loc_cache import LocCache
from tv_extract.gitextractor.extract_complete_file_info import extract_complete_file_info
from tv_extract.util import cli, cd
from tv_extract.util.shell_cmds import getpipeoutput
from tv_extract.data import Revision, RevisionGraph

command_dict = {
    'original_commit': ['git rev-list --max-parents=0 HEAD'],
    'initial_revisions': ['git rev-list --pretty="%T|%H|%at|%ai|%aN|%aE|%P|%s" "HEAD"', 'grep -v ^commit'],
    'master_revisions': ['git rev-list --first-parent --pretty="%T|%H|%at|%ai|%aN|%aE|%P|%s" "HEAD"', 'grep -v ^commit'],
}

def get_revisions(fn_get_output, graph, rev_list_cmds, is_master=False):
    lines = fn_get_output(rev_list_cmds).split('\n')
    for line in lines:
        line = line.strip()
        if line:
            graph.add_revision_to_graph(*get_revision_from_line(line), is_master=is_master)


def extract_revision_graph(cache: LocCache) -> RevisionGraph:
    '''
    Get all revisions from the repo , key them by tree_hash, commit_hash as well as create a graph
    of revisions and a list of revisions merging to master

    :return: RevisionGraph
    '''
    return _extract_revision_graph(cache, getpipeoutput)


def _extract_revision_graph(cache: LocCache, fn_get_output) -> RevisionGraph:
    original_commit = fn_get_output(command_dict['original_commit'])
    graph = RevisionGraph(original_commit)

    get_revisions(fn_get_output, graph, command_dict['initial_revisions'])

    # This gets all commits to master (used to calculate code growth over time). Note that this
    # method isn't foolproof.
    # see: https://stackoverflow.com/questions/15875253/git-log-to-return-only-the-commits-made-to-the-master-branch
    # poke's answer
    get_revisions(fn_get_output, graph, command_dict['master_revisions'], True)

    # now fix up parentage based on what we've seen with the --first-parent logs
    for revision in graph.revisions.values():
        parents = graph.linkage[revision.hash]
        for parent in parents:
            if parent in graph.master_revs:
                revision.master_parent = parent
            else:
                if revision.branch_parent:
                    # This happens when you merge from a branch into this branch (PR on a PR)
                    logging.debug(f"{revision.hash} has multiple branch parents")
                    revision.is_a_pr = False
                revision.branch_parent = parent

    if cache:
        cache.load_from_cache(graph)
    extract_complete_file_info(graph, fn_get_output)
    return graph


def get_revision_from_line(line):
    tree_hash, sha, stamp, time, author, mail, parents, comments = line.split('|', 7)
    try:
        stamp = int(stamp)
    except ValueError:
        stamp = 0
    timezone = time.split(' ')[2]
    domain = '?'
    if mail.find('@') != -1:
        domain = mail.rsplit('@', 1)[1]
    parents = parents.split(' ')
    revision = Revision(sha, stamp, timezone, author, mail, domain, comments)
    return revision, parents


if __name__ == "__main__": # pragma: no cover
    conf, paths, _ = cli.get_cli()
    graphs: Dict[str, RevisionGraph] = {}
    for path in paths:
        repo_name = os.path.split(path)[1]
        with (cd.cd(path)):
            graphs[repo_name] = extract_revision_graph()
    for k, v in graphs.items():
        print(f"{k}: {len(v.revisions)} revisions, {len(v.master_revs)} revisions on master")
