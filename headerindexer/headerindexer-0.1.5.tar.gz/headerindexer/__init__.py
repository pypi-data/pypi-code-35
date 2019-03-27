"""Administrator object to manage data objects and imports, and coordinate operations"""
# todo rewrite function arguments (google style), add type defs

from ._hi_objects import _HeaderIndexerEngine
from typing import Union, List, Dict, Iterable


class HI:
    """A system to bind aliases to indexes of headers in a matrix."""

    def __init__(self, allow_duplicates=True):
        """
        A system to bind aliases to indexes of headers in a matrix.
        """

        self._indexer = _HeaderIndexerEngine()
        """Core services of our header indexing """

        self.allow_duplicates = allow_duplicates
        """Optional setting to allow duplicate header indexes, otherwise will prompt for fix"""

    def run(self, headers: List[str], aliases: Dict[str, Union[str, Iterable]]):
        """Run HeaderIndexer on given sheet_headers list, using head_names dict to generate a
        new nex dict containing header indexes"""

        # Take headers and head_names, and create ndx_calc
        self._indexer.work.gen_ndx_calc(headers, aliases)

        # Begin identifying any errors in the parsing
        self._indexer.check_nonindexed()
        self._indexer.query_fix_nonindexed()

        if not self.allow_duplicates:
            self._indexer.check_duplicates()
            self._indexer.query_fix_duplicates()

        return self._indexer.work.ndx_calc
