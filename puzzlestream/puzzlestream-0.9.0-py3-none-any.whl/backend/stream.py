# -*- coding: utf-8 -*-
"""Stream module.

contains PSStream
"""

import diskcache as dc
from puzzlestream.backend.reference import PSCacheReference


class PSStream(dc.Cache):

    """Subclass of diskcache Cache; the central background harddisk cache."""

    def __init__(self, path: str, *args):
        """Cache init.

        Args:
            path (str): Cache directory.
            *args: All other args, passed to dc.Cache
        """
        super().__init__(path, *args)

    def __contains__(self, key: str) -> bool:
        ID = key.split("-")[0]
        keyn = key[len(ID) + 1:]
        if (super().__contains__(key) and not
                self.__checkIfOutdatedReference(int(ID), keyn)):
            return True
        return False

    def __getitem__(self, key: str) -> object:
        if super().__contains__(key):
            return super().__getitem__(key)
        raise KeyError(key)

    def getItem(self, ID: int, key: str) -> object:
        """Get item from cache.

        Args:
            ID (int): Stream section ID.
            key (str): Requested key.

        Returns:
            Cached data at "ID-key".
        """
        if self.__checkIfOutdatedReference(ID, key):
            raise KeyError(key + " not found for item %d." % (ID))
        return self.__getitem__(str(ID) + "-" + str(key))

    def __checkIfOutdatedReference(self, ID: int, key: str) -> bool:
        item = self.__getitem__(str(ID) + "-" + str(key))

        # delete item if it is a reference to something that no longer exists
        if (isinstance(item, PSCacheReference) and not
                super().__contains__(str(item.sectionID) + "-" + str(key))):
            super().__delitem__(str(ID) + "-" + str(key))
            return True
        return False

    def setItem(self, ID: int, key: str, data: object):
        """Store data in cache.

        Args:
            ID (int): Stream section ID.
            key (str): Key to use.
            data: Data that should be stored; must be pickable!
        """
        super().__setitem__(str(ID) + "-" + str(key), data)
