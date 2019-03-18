import logging

from datetime import datetime
from tv_extract.data import Revision, PullRequest, RevisionGraph


def extract_pr_data(row_processor, graph: RevisionGraph):
    '''
    Given a revision graph, collect information on Pull Requests to master.

    :param row_processor: function to receive the callback
    :return: None
    '''

    for rev in graph.master_revs:
        revision = graph.revisions[rev]
        if revision.is_a_pr:
            branch_rev: Revision = graph.revisions[revision.branch_parent]
            delta = datetime.utcfromtimestamp(revision.stamp) - datetime.utcfromtimestamp(branch_rev.stamp)
            if delta.total_seconds() < 0:
                # This is happening due to time drift on developers laptops
                logging.debug(f"Unexpected. Negative duration: {rev}")
                row_processor(PullRequest(revision.stamp, revision.hash, revision.author,
                                          graph.linkage[rev], revision.branch_parent, rev, -delta))
            else:
                row_processor(PullRequest(revision.stamp, revision.hash, revision.author,
                                          graph.linkage[rev], revision.branch_parent, rev, delta))
