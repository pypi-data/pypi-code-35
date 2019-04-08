"""General utility classes and functions for internal use.
"""


class FileReadError(RuntimeError):
    """Any type of exception during file read
    to be sub-classed for more specific variants depending on file format
    """


class PairedCompItem:
    """Basic input data block, specifying
    ONE response to ONE pair of test stimuli,
    by ONE subject, judging ONE perceptual attribute,
    in ONE test condition, defined by one category label for each Test Factor.
    """
    def __init__(self,
                 subject,
                 attribute,
                 pair,
                 response,
                 test_cond):
        """
        :param subject: string defining subject ID
        :param attribute: string defining perceptual attribute
        :param pair: pair of two stimulus label strings
        :param response: integer in (-M, ..., +M)
        :param test_cond: dict with (test_factor, category) items
        """
        self.subject = subject
        self.attribute = attribute
        self.pair = pair
        self.response = response
        self.test_cond = test_cond

    def __repr__(self):
        return (f'PairedCompItem(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                            for (key, v) in vars(self).items()) +
                '\n\t)')


# ---------------------------------------------------------
def safe_file_path(p):
    """Ensure non-existing file path, to avoid over-writing,
    by adding a sequence number to the path stem
    :param p: file path
    :return: p_safe = similar file path with modified name
    """
    f_stem = p.stem
    f_suffix = p.suffix
    i = 0
    while p.exists():
        i += 1
        p = p.with_name(f_stem + f'-{i}.' + f_suffix)
    return p


# ---------------------------------------------------------
class PairedCompFile:
    """Container of paired-comparison response data
    from one or more listeners,
    one or more Perceptual Attributes,
    in one or more Test Conditions,
    represented as a sequence of PairedCompItem instances.

    This super-class is used mainly for READING a data file.
    It derives test-conditions from path strings,
    to be used as default for test factors that are not defined in the file itself.

    Sub-classes must be defined for each specific file format.
    Sub-classes MUST define an __iter__ method, yielding PairedCompItem instances
    """
    def __init__(self, file_path, pcf):
        """
        :param file_path: Path instance for READING, or None.
            Another path may be defined in the save method.
        :param pcf: (optional) PairedCompFrame instance
        """
        self.file_path = file_path
        self.pcf = pcf

    def __repr__(self):
        return (f'PairedCompFile(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    def path_test_cond(self):
        """Create a dict of test conditions defined by path-string
        """
        if self.pcf is None:
            return dict()
        else:
            return {tf: _find_test_cond_in_path(tc_list, str(self.file_path))
                    for (tf, tc_list) in self.pcf.test_factors.items()}

    def __iter__(self):
        raise NotImplementedError


# ---------------------------------------- private help function:

def _find_test_cond_in_path(tf_categories, path_string):
    """Find test-condition label as sub-string of given path string.
    :param tf_categories: list of possible test-factor category labels
    :param path_string: string
    :return: test_cond = first element in tf_cat_list for which
        a matching sub-string was found in path_string.

    Arne Leijon, 2018-09-09
    """
    def test_cond_in_file(tc, path):
        """Check if tc agrees with file path_string string
        :param tc: test-condition code, string or tuple of strings
        :param path: string path_string
        :return: boolean True if a match was found
        """
        if isinstance(tc, str):
            return tc in path
        elif type(tc) is tuple:
            return all(tc_i in path for tc_i in tc)
        else:
            return False
        # ----------------------------------------

    for tc in tf_categories:
        # if tc in str(path_string):
        # **************** allow tc to be a tuple of strings ???
        if test_cond_in_file(tc, path_string):
            return tc
    return None
