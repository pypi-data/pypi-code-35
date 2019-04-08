import os
import hashlib
import inspect
import pkg_resources

import numpy as np

from . import errors
from .utils import to_numpy, to_numpy_list, uuid
from .container import guess_container
from .filesystem import Dirent

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Collection:
    """Parent object for single file archive collection of multiple disk images

    Instances of this class are not `Segment`s, but instead hold a list of
    `Container`s, each of which will have its own media type and filesystem
    structure, independent of the other disk images.
    """
    pretty_name = "Collection"
    archive_type = "plain file"

    def __init__(self, pathname, data):
        self.containers = []
        self.pathname = pathname
        self.filename = os.path.basename(pathname)
        self.name = ""
        self.unarchive(data)

    @property
    def verbose_info(self):
        lines = []
        name = self.name or self.filename
        lines.append(f"{name}: {self}")
        for c in self.containers:
            lines.append(c.container_info("    "))
        return "\n".join(lines)

    @property
    def basename(self):
        return os.path.basename(self.pathname)

    #### dunder methods

    def __str__(self):
        desc = ""
        if len(self) > 1:
            desc = f"{len(self)} item "
        desc += self.archive_type
        return desc

    def __len__(self):
        return np.alen(self.containers)

    #### compression

    def unarchive(self, byte_data):
        """Attempt to unpack `byte_data` using this archive unpacker.

        Calls `find_containers` to loop through each container found. The order
        listed here will be the order returned by the subclass; no sorting is
        done here.
        """
        for item_data in self.iter_archive(byte_data):
            container = guess_container(item_data)
            container.guess_media_type()
            container.media.guess_filesystem()
            self.containers.append(container)
            container.name = f"Container #{len(self.containers)}"

    def iter_archive(self, byte_data):
        """Return a list of `Container` objects for each item in the archive.

        If the data is not recognized by this subclass, raise an
        InvalidContainer exception. This signals to the caller that a different
        container type should be tried.

        If the data is recognized by this subclass but the unpacking algorithm
        is not implemented, raise an UnsupportedContainer exception. This is
        different than the InvalidContainer exception because it indicates that
        the data was indeed recognized by this subclass (despite not being
        unpacked) and checking further containers is not necessary.
        """
        return [byte_data]

    def archive(self):
        """Pack each container into the archive
        """
        return np_data

    #### iterators

    def iter_segments(self):
        if self.boot is not None:
            yield self.boot
        if self.vtoc is not None:
            yield self.vtoc
        if self.directory is not None:
            yield self.directory

    def iter_dirents(self):
        for container in self.containers:
            for segment in container.media.segments:
                if isinstance(segment, Dirent):
                    yield segment
                yield from segment.yield_for_segment(Dirent)


_collections = None

def _find_collections():
    collections = []
    for entry_point in pkg_resources.iter_entry_points('atrip.collections'):
        mod = entry_point.load()
        log.debug(f"find_collection: Found module {entry_point.name}={mod.__name__}")
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj) and Collection in obj.__mro__[1:]:
                log.debug(f"find_collections:   found collection class {name}")
                collections.append(obj)
    return collections

def find_collections():
    global _collections

    if _collections is None:
        _collections = _find_collections()
    return _collections

def guess_collection(pathname, raw_data, verbose=False):
    collection = None
    for c in find_collections():
        if verbose:
            log.info(f"trying collection {c.archive_type}")
        try:
            collection = c(pathname, raw_data)
        except errors.InvalidCollection as e:
            continue
        else:
            if verbose:
                log.info(f"found collection {c.archive_type}")
            break
    else:
        if verbose:
            log.info(f"image does not appear to be compressed.")
        collection = Collection(pathname, raw_data)
    return collection


def load(pathname):
    sample_data = np.fromfile(pathname, dtype=np.uint8)
    collection = guess_collection(pathname, sample_data)
    return collection
