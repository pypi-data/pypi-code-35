"""
Template for unique Work object, where matrix data is passed to and parsed. Stored
"""

from typing import Dict, List, Union, Iterable


class Work:
    """
    External module of headerIndexer working data. Take in matrix_headers and head_names and gen
    our ndx_calc. No init setup, pass startup data through gen_ndx_calc(matrix_headers, head_names)
    """

    matrix_headers_index_dict: Dict[str, int] = {}
    ndx_calc: Dict[str, Union[int, None]] = {}

    def gen_ndx_calc(self, matrix_headers: List[str], head_names: Dict[str, Union[str, Iterable]]):
        """
        Given a dictionary of header aliases to full header names, and a full row of headers from a
        matrix, create a dictionary of matching aliases with the full header name's column index

        Dictionary with header aliases and calculated indexes is stored as self.ndx_calc, allowing
        any needed parsing without passing

        Args:
            matrix_headers:
                Header row from a matrix i.e. headers on a spreadsheet.
            head_names:
                Header aliases as keys, and full header names as single string or an iterable of
                possible header names.
        """

        self.matrix_headers_index_dict = {head: ndx for ndx, head in enumerate(matrix_headers)}
        """Dictionary of all headers as keys and their enumerated index as values"""

        self.ndx_calc.clear()
        """Dict of all header aliases as keys, and their full header-name index as values"""
        """Dictionary to return; converted from head_names with values traducted to indexes"""

        for reference, headers in head_names.items():

            # Prep to iterate
            if isinstance(headers, (str, bytes, int, float)):
                headers = [headers]

            # Note since reference was a dict key in head_names, each reference should be unique
            try:
                self.ndx_calc[reference] = self._find_col_index(headers)
            except IndexError:
                self.ndx_calc[reference] = None

    def _find_col_index(self, headers: Iterable) -> int:
        """
        Iterate through given possible headers and try to find it's column index. Returns first
        found index, or raises IndexError if no matches were found in the header row

        Args:
            headers:
                Iterable sequence of possible headers (i.e. [Hostname, DNSHostnames, serverIDs] )

        Returns:
                First found header name's index
        """
        for header in headers:
            try:
                return self.matrix_headers_index_dict[header]
            except KeyError:
                pass
        raise IndexError
