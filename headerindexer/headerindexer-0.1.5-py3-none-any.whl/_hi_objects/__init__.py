"""HeaderIndexer Engine"""

from .data_obj import DF_BUILD
from typing import Union


class _HeaderIndexerEngine:
    """
    Engine to hold work and errors objects, and functions to check and fix errors.
    Actual HeaderIndexer runs commands from above
    """

    def __init__(self):

        self.work = DF_BUILD.new_work_obj()
        """Primary helper to create and store ndx_calc"""
        self.errors = DF_BUILD.new_errors_obj()
        """Dataclass for _error_string, _nonindexed, and _duplicates. Resets each run()"""
        self.pycolims = None
        """Reference call for pycolims to import to. Assign if/when needed"""

    # # # Fix Non indexed

    def check_nonindexed(self):
        """Checks for any aliases not indexed"""
        for key, val in self.work.ndx_calc.items():
            if val is None:
                self.errors.nonindexed.append(key)

    def query_fix_nonindexed(self):
        """Simple check from user to fix nonindexed aliases"""
        print(f'{len(self.errors.nonindexed)} non indexed aliases:\n')
        print('\n'.join(x for x in self.errors.nonindexed), '\n')
        print('Manually assign?')
        print('  (0) Yes')
        print('  (1) No, leave as is (Not recommended!)')
        print('  (2) No, exit script')
        ans = input('> ')
        if ans == '0':
            self._fix_nonindexed()
        elif ans == '2':
            self._raise_value_error()

    def _fix_nonindexed(self):
        """Interactive script to fix non-indexed aliases, one by one"""
        for non_indexed in self.errors.nonindexed:
            self._menu_prompt(non_indexed)
        self.errors.nonindexed.clear()

    # # # Fix duplicates

    def check_duplicates(self):
        """Checks for any aliases with duplicate indexes"""
        dup_check = {}
        # Create a reverse dict of found index #s, with bound aliases in a gen_ndx_calc as values
        for reference, index in self.work.ndx_calc.items():
            dup_check.setdefault(index, set()).add(reference)

        # Check if any indexes correspond to more than one alias
        for index, bound_aliases in dup_check.items():
            if len(bound_aliases) > 1:
                for ref in bound_aliases:
                    self.errors.duplicates[ref] = index

    def query_fix_duplicates(self):
        """Simple check from user to fix aliases with duplicate indexes"""
        print(f'{len(self.errors.duplicates)} aliases with duplicate indexes:\n')
        print('\n'.join(f'{key}: {val}' for key, val in self.errors.duplicates.items()))
        print()
        print('Manually assign?')
        print('  (0) Yes')
        print('  (1) No, leave as is (Not recommended!)')
        print('  (2) No, exit script')
        ans = input('> ')
        if ans == '0':
            self._fix_duplicates()
        elif ans == '2':
            self._raise_value_error()

    def _fix_duplicates(self):
        """Interactive script to fix duplicated aliases, one by one"""
        for duplicate in self.errors.duplicates:
            self._menu_prompt(duplicate)
        self.errors.duplicates.clear()

        # Check for new/remaining duplicates. Recursively fix
        self.check_duplicates()
        if self.errors.duplicates:
            self.query_fix_duplicates()

    # # # Shared tools

    def _menu_prompt(self, alias: Union[str, int, bytes]):
        """Use menu system and matrix_headers_index_dict to have user manually choose a header for
        a given alias. Note that this does not remove the alias from the errors iterable, just
        assigns the index to ndx_calc

        Args:
            alias: Alias for user to manually assign
        """
        # Ensure pycolims single is properly imported
        if not self.pycolims:
            from .pycolims_0_2_0 import Single
            self.pycolims = Single()
        prompt = f"Select header for alias: {alias}"
        # prompt user with a list of all headers, for them to assign the reference to
        chosen_header = self.pycolims.run(self.work.matrix_headers_index_dict, prompt)
        # Get that header's actual column index
        self.work.ndx_calc[alias] = self.work.matrix_headers_index_dict[chosen_header]

    def _raise_value_error(self):
        """Raises ValueError if needed (Nonindexed values, duplicates)"""
        if self.errors.nonindexed:
            self._add_to_error_string("Non indexed headers!", self.errors.nonindexed)
        if self.errors.duplicates:
            self._add_to_error_string("Duplicate header indexes!", self.errors.duplicates)
        if self.errors.error_exists:
            raise IndexError(self.errors.errstr)

    def _add_to_error_string(self, header: str, error_arr: Union[dict, list]):
        """Funnel function to concatenate an error string to self.errors.errstr"""
        self.errors.errstr += header + '\n'
        self.errors.errstr += '\n'.join(f'    {x}' for x in error_arr) + '\n'
