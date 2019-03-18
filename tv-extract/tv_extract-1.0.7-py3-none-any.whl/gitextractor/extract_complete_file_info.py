import csv
import logging
import os

from ordered_set import OrderedSet
from typing import Iterable
from tv_extract.util import cli, cd
from tv_extract.data import FileInfo, Revision, RevisionGraph
from tv_extract.gitextractor import extract_revision_graph


def collect_file_info(revision_set: Iterable[Revision], fn_get_output):
    total = 0
    cache = 0
    for revision in revision_set:
        total += 1
        if not revision.file_infos:
            logging.info(f"git checkout {revision.hash}")
            fn_get_output([f'git checkout {revision.hash} >/dev/null 2>&1'])
            # for some reason if we combine these, tokei gives incorrect results!!!!
            lines = fn_get_output(['tokei']).split('\n')
            if len(lines) > 3:
                if 'Note: ' in lines[0]:
                    lines = lines[1:]
                for line in lines[3:-3] + [lines[-2]]:
                    line = line.strip()
                    file_info = FileInfo(*line.rsplit(maxsplit=5))
                    revision.file_infos[file_info.language] = file_info
            else:
                debug = '\n'.join(lines)
                logging.warning(f"Unexpected results from tokei: \n{debug}")
        else:
            cache += 1
    logging.info(f"Total revisions: {total}. {cache} found in cache")


def collect_deltas(graph, revision_set):
    for rev_hash in revision_set:
        revision = graph.revisions[rev_hash]
        current = revision.file_infos
        if current:
            if revision.original_commit:
                for lang, cur_file_info in current.items():
                        revision.delta[lang] = cur_file_info
            else:
                parent = get_parent(revision)
                if parent:
                    previous = graph.revisions[parent].file_infos
                    if previous:
                        for lang, cur_file_info in current.items():
                            if lang in previous:
                                revision.delta[lang] = cur_file_info - previous[lang]
                            else:
                                revision.delta[lang] = cur_file_info
                    else:
                        logging.warning(f"WARNING: No file info for commit: {graph.revisions[parent].hash}.")
                else:
                    logging.warning(f"WARNING: No parent for commit: {revision.hash}.")
        else:
            logging.warning(f"WARNING: No file info for commit: {revision.hash}.")


def get_parent(revision: Revision):
    # favor master on a merge
    if revision.master_parent:
        return revision.master_parent
    return revision.branch_parent


def extract_complete_file_info(graph: RevisionGraph, fn_get_output):
    '''
    Given a revision graph, collect all file info
    using tokei for those revisions

    :param: graph - Revision Graph

    :return: None. As a side effect, compliete file info by language type will be added to all
    revisions in master_rev
    '''

    # We use a custom .mailmap file to resolve autors. That was great while
    # we collected revision info (extract_revision_graph), but will block our ability to
    # checkout individual revisions, therefor, clear the .mailmap checkout (if it exists)
    fn_get_output(['git checkout -- .mailmap >/dev/null 2>&1'])

    collect_file_info(graph.revisions.values(), fn_get_output)
    fn_get_output(['git checkout master >/dev/null 2>&1'])

    collect_deltas(graph, OrderedSet.union(graph.master_revs, graph.not_a_merge))

if __name__ == "__main__": # pragma: no cover
    conf, paths, outputpath = cli.get_cli()

    with open(outputpath, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['repo', 'hash', 'stamp', 'author', 'language', 'files', 'lines', 'code', 'comments', 'blanks'])

        for path in paths:
            repo_name = os.path.split(path)[1]
            with (cd.cd(path)):
                graph = extract_revision_graph()
                extract_complete_file_info(graph)

                for rev in graph.master_revs:
                    revision: Revision = graph.revisions[rev]
                    for lang, file_info in revision.delta.items():
                        if file_info.file_count or \
                                file_info.line_count or \
                                file_info.code_line_count or \
                                file_info.comment_line_count or \
                                file_info.blank_line_count:
                            writer.writerow([repo_name,
                                             revision.hash,
                                             revision.stamp,
                                             graph.revisions[revision.branch_parent].author,
                                             lang,
                                             file_info.file_count,
                                             file_info.line_count,
                                             file_info.code_line_count,
                                             file_info.comment_line_count,
                                             file_info.blank_line_count])
