"""Functions to read Paired-comparison test results,
stored in file format defined by Martin Dahlquist, 2002.

NOTE: Originally, this file format always assumed forced_choice = True,
so the forced_choice parameter is NOT stored in the file.
However, later use may allow data with forced_choice = False,
so the file contents is now interpreted depending on the given parameter


*** Version History:
2018-09-30, sub-class of PairedCompFile, iterator of PairedCompItem objects
2018-11-25, changed name systems -> objects
2018-12-08, Warning in case file data does not agree with given PairedCompFrame instance.
"""

# *** allow save in res format ???

from PairedCompCalc import pc_base
import logging

logger = logging.getLogger(__name__)


# ------------------------------------------ Exception:
class FileFormatError(RuntimeError):
    """Signal any form of file format error when reading
    """


# ----------------------------------------------------------------
class PairedCompFile(pc_base.PairedCompFile):
    """PairedCompFile variant to read / write a *.res file
    containing paired-comparison results
    for ONE subject and ONE perceptual attribute,
    in test-conditions specified only by file path-string.
    """
    def __init__(self,
                 file_path,
                 pcf,
                 contents=None,
                 **kwargs):
        """
        :param file_path: path for existing *.res file
        :param pcf: a PairedCompFrame instance.
            NOTE: pcf.forced_choice determines how file response data are interpreted!!!
        :param contents: (optional) dict with all (key, value) pairs for this format
        :param kwargs: any additional params, NOT USED
        """
        super().__init__(file_path, pcf)
        if contents is None:  # read from file
            with open_encoded_txt(self.file_path) as f:
                self.contents = load(f, self.pcf.forced_choice)
            self._check_contents()
        else:  # just prepare to save contents to file
            self.contents = contents

    def __repr__(self):
        return (f'PairedCompFile(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                            for (key, v) in vars(self).items()) +
                '\n\t)')

    def __iter__(self):
        """generator of PairedCompItem instances,
        one for each result row in file
        """
        subject = self.contents['subject']
        attr = self.contents['attribute']
        test_cond = self.path_test_cond()
        for sr in self.contents['result']:
            yield pc_base.PairedCompItem(subject, attr, *sr, test_cond)

    def save(self, f_name, dir):
        """Save contents in .res format
        *** Not recommended, use json instead.
        :param f_name:
        :param dir:
        :return:
        """
        raise NotImplementedError

    def _check_contents(self):
        """check self.contents vs. self.pcf expected values.
        :return: None
        result: logger warnings for any potentially serious disagreement
        """
        if self.contents is not None:
            if self.pcf.difference_grades is not None:
                if self.pcf.difference_grades != self.contents['difference_grades']:
                    logger.warning(f'Unexpected difference grades in {self.file_path}')


# def save(pcr, f, pcf):  # ***********************************
#     """Save self.contents in old 2002 format
#     :param pcr: one pc_data.PairedCompRecord instance
#     :param f: open file object for writing
#     :return: None
#     NOTE: this does not handle test_factors !
#     """
#     # convert it to old-class object
#     pcr2002 = PairedCompRecord2002(subject=pcr.subject,
#                                    objects=pcr.objects,
#                                    attribute=pcr.attribute,
#                                    result=pcr.result,
#                                    **pcr.othr)
#
#     pcr_dict = {'PairedCompRecord': pcr2002.__dict__}
#     dump(pcr_dict, f, pcf.forced_choice)

# def dump(session_dict, f, forced_choice):
#     """write a complete result for one PairedCompRecord2002
#     in ORCA text format, as defined by Dahlquist, 2002
#     :param session_dict: { 'PairedCompRecord': s }, where
#         s includes properties for one PairedCompRecord2002 object,
#         obtained, e.g., as s.__dict__
#     :param f: file-like object, allowing f.write() operations
#         If already existing, the f is over-written without warning
#     :param forced_choice: boolean = pc_data.PairedCompFrame.forced_choice
#     :return: None
#     Exceptions: KeyError is raised if session_dict does not include required data.
#     """
#     s = session_dict['PairedCompRecord']
#     with f:
#         f.write(s['comment'] + '\n')
#         f.write(s['subject'] + '\n')
#         # t = s.time_stamp
#         f.write(s['time_stamp'] + '\n')
#         f.write(s['attribute'] + '\n')
#         difference_grades = s['difference_grades']
#         f.write(''.join('\"' + m + '\"\n' for m in difference_grades))
#         objects = s['objects']
#         n_objects = len(objects)
#         f.write(f'{n_objects},{len(difference_grades)},2\n')
#         f.write(''.join(sys +'\n' for sys in objects))
#         f.write('\"matris\"\n')
#         # ***** calculate summary matrix ********************
#         for n in range(n_objects):
#             f.write(','.join(['0' for m in range(n_objects)]) + '\n')
#             # *** just a zero matrix, not used for analysis anyway
#         result = s['result']
#         f.write('\"antal stimuli\"\n' +
#                 f'{len(result)}\n')
#         f.write('\"Stim1\",\"Stim1\",\"Resp\",\"Rate\",\"Rep\"\n')
#         for sr in result:
#             ((a, b), r) = sr[0:2]
#             (i, j) = (objects.index(a), objects.index(b))
#             choice = (0 if r == 0 else 2 if r > 0 else 1)
#             # magn = abs(r) if s['forced_choice'] else 1 + abs(r)
#             magn = abs(r) if forced_choice else 1 + abs(r)
#             # NOTE: for historical reasons, magn must be
#             # index into difference_grades, using MatLab:s origin-one indexing.
#             # Therefore, magn must always be 1, 2, etc. never = 0.
#             f.write(f'{1+i},{1+j},{choice},{magn},0\n')


def load(f, forced_choice):
    """Read one file saved in old res format
    as defined by Martin Dahlquist, 2002
    :param f: open file object, allowing r.readline() operations
    :param forced_choice: boolean switch
    :return: dict with PairedCompRecord attributes from file,
        OR None, if any error encountered
    """
    def clean(s):
        """strip away unwanted characters from a string
        :param s: string
        :return: cleaned string
        """
        clean_s = s.strip('\n\"')
        if len(clean_s) == 0:
            raise FileFormatError(f'Unexpected empty line in {f_name}')
        else:
            return clean_s

    def decode_res(r, objects):
        """recode response item from res format to new StimRespItem standards
        :param r: one paired-comparison result line (stim_1, stim_2, choice, magn)
        :param objects: list of string labels, corresponding to system indices in r
        :return: tuple (pair, response) in StimRespItem format, where
            pair = tuple of system string labels (A, B) for presented pair
            response = integer in {- max_difference,..., + max_difference}
        """
        (i,j, choice, m) = r[:4]
        pair = (objects[i-1], objects[j-1])  # index origin 1 in res file
        # m = (0 if choice == 0 else m-1 if forced_choice else m)
        if choice == 0:
            m = 0
        elif not forced_choice:
            m -= 1  # invert the change in function dump
        if choice == 1:
            m = - m
        elif choice < 0 or choice > 2:
            raise FileFormatError(f'Illegal choice value in result in {f_name}')
        return pair, m  #, tc
    # -----------------------------------------
    f_name = f.name
    # test_cond = decode_test_condition(f_name, test_factors)
    s = dict()  # dict for result
    with f:
        s['comment'] = clean(f.readline())
        s['subject'] = clean(f.readline())
        s['time_stamp'] = clean(f.readline())
        a = clean(f.readline())
        a = a.replace('\"', '')
        a = a.replace(',', ' ')
        s['attribute'] = a.split(sep=' ')[0]
        s['difference_grades'] = r_labels = []
        while True:
            l = f.readline()
            if 0 == l.find('\"'):
                r_labels.append(clean(l))
            else:
                nsr = [int(n) for n in l.split(sep=',')]
                (n_objects, n_resp) = nsr[:2]
                break
        if n_resp != len(r_labels):
            raise FileFormatError(f'Inconsistent number of response labels in {f_name}')
            # ******* logger.warning is enough ?
        s['objects'] = objects = [clean(f.readline())
                                  for n in range(n_objects)]
        if 0 != (f.readline()).find('\"matr'):
            raise FileFormatError(f'matrix label not found in {f_name}')
        s['summary'] = [[int(n) for n in f.readline().split(sep=',')]
                        for n in range(n_objects)]
        l = f.readline()
        if (0 != l.find('\"num') and
            0 != l.find('\"ant')):
            raise FileFormatError(f'Number of results not found in {f_name}')
        n_pres = int(f.readline())
        s['result'] = result = []
        l = f.readline()
        if 0 != l.find('\"Stim'):
            raise FileFormatError(f'Unexpected result header in {f_name}')
        l = f.readline()
        while 0 < len(l):  # read until EOF
            r = [int(n) for n in l.split(sep=',')]
            result.append(decode_res(r, objects))  # ************ test_cond))
            l = f.readline()
        if n_pres != len(result):
            raise FileFormatError(f'Inconsistent number of results in {f_name}')
        # if any(abs(r[1]) >= len(r_labels) for r in result):
        #     raise FileFormatError(f'Response outside difference_grades in {f_name}')
        # ****** this check must consider forced_choice *******
        if forced_choice and any(r[1] == 0 for r in result):
            raise FileFormatError(f'Expected forced_choice, but found zero response in {f_name}')
        return s
        # --------------------- OK: whole file has been read without problem


def open_encoded_txt(path):
    """Try to open a text file with a working encoding
    :param path: Path object or path string identifying a file
    :return: open file object
        OR None, if no working encoding was found

    Method: just try some encodings until a working one is found
    """
    encodings = ['utf-8', 'ISO-8859-1']
    for enc in encodings:
        try:
            with open(path, mode='rt', encoding=enc) as f:
                l = f.read()
            # No error: OK
            return open(path, mode='rt', encoding=enc)
            # open it again with right encoding
        except ValueError as e:
            pass  # try next encoding instead
    raise FileFormatError(f'Unknown text encoding in {path}')

