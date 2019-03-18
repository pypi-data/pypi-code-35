from dataclasses import dataclass, field
from typing import Dict, List
from ordered_set import OrderedSet
from tv_extract.data.revision import Revision

@dataclass
class RevisionGraph:
    original_commit: str
    revisions: Dict[str, Revision] = field(default_factory=lambda: {})
    linkage: Dict[str, List[str]] = field(default_factory=lambda: {})
    master_revs: OrderedSet = field(default_factory=lambda: OrderedSet())
    not_a_merge: OrderedSet = field(default_factory=lambda: OrderedSet())
    merges: OrderedSet = field(default_factory=lambda: OrderedSet())


    def add_revision_to_graph(self, revision: Revision, parents: List[str], is_master: bool):
        if not revision.hash in self.revisions:
            self.revisions[revision.hash] = revision
        if not revision.hash in self.linkage:
            self.linkage[revision.hash] = parents
        if is_master:
            if len(parents) == 2:
                self.revisions[revision.hash].is_a_pr = True
            self.master_revs.add(revision.hash)
        if len(parents) <= 1:
            self.not_a_merge.add(revision.hash)
        elif len(parents) == 2:
            self.merges.add(revision.hash)
        if revision.hash == self.original_commit:
            self.revisions[revision.hash].original_commit = True
