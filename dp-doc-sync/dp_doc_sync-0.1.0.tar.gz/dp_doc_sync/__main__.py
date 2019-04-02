#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 zenbook <zenbook@zenbook-XPS>
#
# Distributed under terms of the MIT license.

"""

"""

import os
import fire
import logging
import kanilog
import stdlogging
import subprocess
import mkdir_p
from pathlib import Path


def main(id_file, key_file, address, sync_folder, sync_all=False):
    sync_folder = Path(sync_folder).expanduser().absolute()
    base_command = 'dptrp1 --client-id %s --key %s --addr %s'%(id_file, key_file, address)
    id_file = Path(id_file).expanduser()
    key_file = Path(key_file).expanduser()

    result = str(subprocess.check_output('%s list-documents' % base_command, shell=True), 'utf8')
    remote_documents = [Path(path.replace('Document/', '')) for path in result[:-1].split('\n')]

    # --  Download Document
    for document in remote_documents:
        parent_folder = sync_folder / document.parent
        if not parent_folder.exists():
            mkdir_p.mkdir_p(parent_folder)
        target_file = sync_folder / document
        if not target_file.exists() or sync_all:
            logging.info('Downloading %s', document)
            subprocess.check_output('%s download "Document/%s" "%s"' % (base_command, str(document), str(target_file)), shell=True)

    # -- Upload Document
    for file_path in sync_folder.glob('**/*.pdf'):
        relative_path = file_path.relative_to(sync_folder)
        if relative_path not in remote_documents:
            logging.info('Uploading %s', file_path)
            subprocess.check_output('%s upload "%s" "Document/%s"' % (base_command, str(file_path), str(relative_path)), shell=True)


if __name__ == "__main__":
    kanilog.setup_logger(logfile='/tmp/%s.log' % (Path(__file__).name), level=logging.INFO)
    stdlogging.enable()
    fire.Fire(main)
