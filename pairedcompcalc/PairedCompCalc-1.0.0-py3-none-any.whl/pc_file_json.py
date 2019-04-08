"""This module defines class PairedCompFile to
read / write paired-comparison data in serialized json file format.
One file may include several PairedCompItem instances,
for one or more subjects and one or more test-conditions.

*** Version History:
2018-09-25, first functional version
2018-12-08, PairedCompFile.save() method, creating safe file name to avoid over-writing
2019-03-30, PairedCompFile.save() with allow_over_write argument
"""

from pathlib import Path
import json
import logging

from . import __version__
from . import pc_base


logger = logging.getLogger(__name__)


class FileFormatError(pc_base.FileReadError):
    """Any type of input file format error"""


# ---------------------------------------------------------
class PairedCompFile(pc_base.PairedCompFile):
    """File storing paired-comparison experimental results
    from one or more listeners, in one or more test conditions,
    represented as a sequence of PairedCompItem instances.
    This class is used mainly to read / write a json file,
    as a flat sequence of PairedCompItem instances.
    """
    def __init__(self, items=None, file_path=None, pcf=None, **kwargs):
        """
        :param items: (optional) list of PairedCompItem instances.
        :param file_path: (optional) Path instance for READING
            Another path may be defined in the save method.
        :param pcf: (optional) PairCompFrame instance
        :param kwargs: other keyword arguments, not used
        """
        super().__init__(file_path, pcf)
        if items is None and file_path is not None:
            # self is used for READING
            items = self.load()
        self.items = items

    def __repr__(self):
        return (f'PairedCompFile(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    def __iter__(self):
        """Iterate over all items loaded from a file
        """
        path_test_cond = self.path_test_cond()
        for r in self.items:
            # merge path test-cond with test-cond loaded from file:
            test_cond = path_test_cond.copy()
            test_cond.update(r.test_cond)
            r.test_cond = test_cond
            yield r

    def load(self):
        """Load paired-comparison data from given file.
        :return: items = list of PairedCompItem instances loaded from file
        """
        try:
            with self.file_path.open() as f:
                file_dict = json.load(f)
            if 'PairedCompRecord' in file_dict.keys():
                # version 0.8 format
                file_dict = _update_version_format(file_dict['PairedCompRecord'])
            elif 'PairedCompFile' in file_dict.keys():
                file_dict = _update_version_format(file_dict['PairedCompFile'])
            return [pc_base.PairedCompItem(**r) for r in file_dict['items']]
        except (KeyError, json.decoder.JSONDecodeError):
            raise pc_base.FileReadError(f'File {self.file_path} does not contain PairedComp data')

    def save(self, file_name=None, dir='.', allow_over_write=False):
        """Save self.items to file
        :param dir: (optional) path to directory for saving
        :param file_name: (optional) file name
        :param allow_over_write: boolean switch, =True allows old file to be over-written
        :return: None
        """
        dir = Path(dir)
        dir.mkdir(parents=True, exist_ok=True)
        # make sure it exists, create new hierarchy if needed
        if file_name is None:
            if self.file_path is not None:
                file_name = self.file_path.name
            else:
                file_name = self.items[0].subject
        if allow_over_write:
            # no file-name check, over-write if file already exists
            file_path = (dir / file_name).with_suffix('.json')
        else:
            file_path = pc_base.safe_file_path((dir / file_name).with_suffix('.json'))
        # = non-existing file, to avoid over-writing
        self_dict = {'items': [i.__dict__ for i in self.items],
                     '__version__': __version__}
        with open(file_path, 'wt') as f:
            json.dump({'PairedCompFile': self_dict}, f, ensure_ascii=False, indent=1)
        self.file_path = file_path


# ------------------------------------------------ internal module help functions

def _update_version_format(p_dict):
    """Update contents from an input json file to fit current file version
    :param p_dict: an old PairedCompRecord dict saved with an old package version
    :return: new_dict = dict with current file format
    """
    if p_dict['__version__'] < '0.9.0':
        try:
            subject = p_dict['subject']
            attr = p_dict['attribute']
            items = [{'subject': subject,
                      'attribute': attr,
                      'pair': r[0],
                      'response': r[1],
                      'test_cond': r[2]}
                     for r in p_dict['result']]
        except KeyError:
            raise FileFormatError('Error converting old "PairedCompRecord" file format')
        return {'items': items}
    # elif p_dict.__version__ < '1.0.0':  *** future
    #
    else:
        return p_dict  # no change for files in newer format
