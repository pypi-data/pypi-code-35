import abc
import logging
import pickle
from pathlib import Path
from tv_extract.data.revision_graph import RevisionGraph

class LocCache:
    @abc.abstractmethod
    def load_from_cache(self, graph: RevisionGraph):
        pass

    @abc.abstractmethod
    def save_to_cache(self, graph: RevisionGraph):
        pass


class PickleCache(LocCache): # pragma: no cover
    def __init__(self, cache: Path):
        self.cache = cache

    def load_from_cache(self, graph: RevisionGraph):
        if self.cache.exists():
            cache_data = pickle.load(self.cache.open(mode='rb'))
            for key, data in cache_data.items():
                if key in graph.revisions:
                    graph.revisions[key].file_infos = data[0]
                else:
                   logging.warning(f"{key} not found in git revisions. This shouldn't happen. Please investigate.")

    def save_to_cache(self, graph: RevisionGraph):
        cache_data = {}  # key by revision id, values tuple of: file_infos and deltas
        for key, revision in graph.revisions.items():
            if revision.file_infos or revision.delta:
                cache_data[key] = [revision.file_infos, revision.delta]
        pickle.dump(cache_data, self.cache.open(mode='wb'))
