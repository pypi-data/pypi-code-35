"""Storage for errors or non-found indexes. Reset on each run"""

from typing import List, Dict


class Errors:
    """Storage for errors or non-found indexes. Includes reset function"""

    errstr: str = ''
    """Error string, to be stderr (dependant on self._settings.raise_error)"""
    nonindexed: List[str] = []     # Non active
    """Dict of reference headers that were not found in self.sheet_headers"""
    duplicates: Dict[str, int] = {}
    """Dict of reference headers that were found more than once"""

    def set(self):
        """Sets all Error holders to default"""
        self.errstr.replace(self.errstr, '')
        self.nonindexed.clear()
        self.duplicates.clear()

    @property
    def error_exists(self) -> bool:
        """"Bool flag indicating if any entries in self.nonindexed or duplicates"""
        return any((self.nonindexed, self.duplicates))
