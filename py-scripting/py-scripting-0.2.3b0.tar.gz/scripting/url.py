#! /usr/bin/env python
import os
import shutil

from six.moves import urllib

from .unix import checksum


def download_url(url, dest, md5=None, cache="."):
    dest = os.path.abspath(os.path.join(cache, dest))

    if os.path.exists(dest):
        if md5 and checksum(dest) == md5:
            return dest
        else:
            os.remove(dest)

    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        raise
    except urllib.error.URLError:
        raise
    else:
        with open(dest, "w") as destination:
            shutil.copyfileobj(response, destination)

    return os.path.abspath(dest)
