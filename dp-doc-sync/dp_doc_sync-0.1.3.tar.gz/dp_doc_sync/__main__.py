#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 zenbook <zenbook@zenbook-XPS>
#
# Distributed under terms of the MIT license.

"""

"""

import datetime
import logging
import os
import pickle
import subprocess
import time
from pathlib import Path

import dateutil.parser
import fire
import kanilog
import mkdir_p
import stdlogging
from dateutil import tz
from dptrp1.dptrp1 import DigitalPaper


def download(dp, entry_path, target_file, entry_timestamp):
    logging.info('Downloading %s', entry_path)
    data = dp.download(str(entry_path))
    target_file.write_bytes(data)
    os.utime(target_file, (entry_timestamp, entry_timestamp))


def main(id_file, key_file, address, sync_folder, sync_all=False):
    sync_folder = Path(sync_folder).expanduser().absolute()
    last_sync_timestamp_file = sync_folder.parent / 'last_sync_timestamp'
    if last_sync_timestamp_file.exists():
        last_sync_timestamp = int(last_sync_timestamp_file.read_text())
    last_dpaper_pathes = []
    last_dpaper_pathes_file = sync_folder.parent / 'last_dpaper_pathes'
    if last_dpaper_pathes_file.exists():
        last_dpaper_pathes = pickle.loads(last_dpaper_pathes_file.read_bytes())

    base_command = 'dptrp1 --client-id %s --key %s --addr %s' % (id_file, key_file, address)
    id_file = Path(id_file).expanduser()
    client_id = id_file.read_text().strip()
    key_file = Path(key_file).expanduser()
    key = key_file.read_text()

    result = str(subprocess.check_output('%s list-documents' % base_command, shell=True), 'utf8')
    remote_documents = [Path(path.replace('Document/', '')) for path in result[:-1].split('\n')]

    dp = DigitalPaper(address)

    dp.authenticate(client_id, key)
    remote_documents = dp.list_documents()

    # --  Download Document
    for document in remote_documents:
        entry_path = Path(document['entry_path'])
        parent_folder = sync_folder / entry_path.parent
        if not parent_folder.exists():
            mkdir_p.mkdir_p(parent_folder)
        target_file = sync_folder / Path(str(entry_path).replace('Document/', ''))
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        dt = dateutil.parser.parse(document['modified_date']).astimezone(to_zone)
        entry_timestamp = int((time.mktime(dt.timetuple()) + dt.microsecond / 1000000.0))
        if not target_file.exists() or sync_all:
            if entry_timestamp > last_sync_timestamp:
                download(dp, entry_path, target_file, entry_timestamp)
            else:
                logging.info('Deleting Document %s', entry_path)
                dp.delete_document(str(entry_path))
        else:
            entry_timestamp = int((time.mktime(dt.timetuple()) + dt.microsecond / 1000000.0))
            target_file_timestamp = int(os.path.getmtime(target_file))
            if document['created_date'] != document['modified_date']:
                if target_file_timestamp < entry_timestamp:
                    download(dp, entry_path, target_file, entry_timestamp)

    # -- Upload Document
    remote_document_pathes = [Path(document['entry_path']) for document in remote_documents]
    for file_path in sync_folder.glob('**/*.pdf'):
        relative_path = 'Document' / file_path.relative_to(sync_folder)
        if relative_path not in remote_document_pathes:
            if relative_path not in last_dpaper_pathes:
                logging.info('Uploading %s', relative_path)
                dp.upload(file_path.read_bytes(), str(relative_path))
            else:
                logging.info('Delete host document %s', file_path)
                file_path.unlink()

    last_sync_timestamp_file.write_text(str(int(time.time())))
    last_dpaper_pathes_file.write_bytes(pickle.dumps(remote_document_pathes))


if __name__ == "__main__":
    kanilog.setup_logger(logfile='/tmp/%s.log' % (Path(__file__).name), level=logging.INFO)
    stdlogging.enable()
    fire.Fire(main)
