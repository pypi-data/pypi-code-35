import errno
import hashlib
import os
from functools import partial

import requests
from six.moves.urllib_parse import urlparse


def hash_file(file, block_size=65536):
    hash_ = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hash_.update(buf)

    return hash_.hexdigest()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_filename_from_url(url):
    return urlparse(url).path.split('/')[-1]


def download_file(url, filepath=None):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    if filepath is None:
        # TODO: decode url, get filename
        filepath = get_filename_from_url(url)

    with open(filepath, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)
