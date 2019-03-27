""" A minimal lock file mechanism, creating a temporary file to signal that a
specific file should not be touched.
"""
import os
import errno


class ResourceLocked(Exception):
    """ This file, folder, etc was already locked """
    pass


class LockFile(object):

    def __init__(self, filename):
        self.filename = filename

    @getter
    def lockfile(self):
        return self.filename + "~lock"

    def __enter__(self):
        # Test for existence with os.open, to avoid race conditions
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            self.file_handle = os.open(self.lockfile, flags)
        except OSError as e:
            if e.errno == errno.EEXIST:  # Failed as the file already exists.
                raise ResourceLocked("%s is used by another process" %
                                     self.filename)
            else:
                # Something went wrong, reraise
                raise
        finally:
            os.close(self.file_handle)

    def __exit__(self, type, value, tb):
        if os.path.exists(self.lockfile):
            os.unlink(self.lockfile)
        else:
            raise Exception("Could not find a lock-file to delete. \
Please verify the data integrity of %s" % self.filename)
