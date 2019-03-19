# -*- coding: utf-8 -*-
"""
File storage manager

Provides tools to store payment datas in csv format with automatic history
control tokens
"""
import hashlib


class FileContext(object):
    def __init__(self, fpath):
        self.file_path = fpath

    def _compute_previous_entry_hash(self):
        """
        Compute the hash of the last history entry

        :rtype: str
        """
        result = ""
        with open(self.file_path, 'r') as fbuf:
            last_line = fbuf.read.splitlines[-1]
            result = hashlib.sha1(last_line).hexdigest()
        return result

    def store(self, record):
        """
        Stores a record in the current file

        :param dict record: The record to store
        """
        record['previous_entry_hash'] = self._compute_previous_entry_hash()

        with open(self.file_path, 'a') as fbuf:
            fbuf.write(record.as_csv())
        return True
