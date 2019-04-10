# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from contextlib import contextmanager

from ._dump import Dump
from ._exceptions import (
    ExcessMemoryError,
    ImplementationError,
    InsufficientMemoryError,
    UnpackError,
)


class Memory:

    """Memory unpack manager.

    :param bytes-like buffer: memory bytes to manage

    """

    def __init__(self, buffer):
        self._buffer = memoryview(buffer)
        self.consumed = 0
        self.nbytes = self._buffer.nbytes

    @property
    def buffer(self):
        """Memory byte buffer.

        :returns: memory bytes buffer
        :rtype: memoryview

        """
        return self._buffer

    @property
    def available(self):
        """Number of memory bytes not yet consumed.

        :returns: number of unconsumed memory bytes
        :rtype: int

        """
        return self.nbytes - self.consumed

    @contextmanager
    def limit(self, nbytes):
        """Provide context under which available memory bytes is limited.

        Under returned context, limit the number of bytes reported by the
        ``available`` property as well as those available through the
        ``consumed_bytes`` method to the specified limit (or the end of
        the buffer, whichever is less).

        :param int nbytes:
            number of bytes beyond the already consumed bytes to limit
            memory consumption to

        """
        original_nbytes = self.nbytes

        end = self.consumed + nbytes
        if end < original_nbytes:
            self.nbytes = end

        try:
            yield self
        finally:
            self.nbytes = original_nbytes

    def unpack_and_getdump(self, cls):
        """Unpack item from memory bytes and get packed memory summary.

        :param type cls: item class
        :returns: item, dump
        :rtype: cls, Dump

        """
        dump = Dump(access='x')

        try:
            item = cls.__unpack__(self, dump, None)

        except InsufficientMemoryError as exc:
            raise InsufficientMemoryError(
                f'\n\n{dump.get_table()}\n\nInsufficientMemoryError: {exc}, '
                f'dump above shows interrupted progress',
                *exc.args[1:]).with_traceback(exc.__traceback__)

        except Exception as exc:
            raise UnpackError(
                f"\n\n{dump.get_table()}"
                f"\n\nUnpackError: unexpected {type(exc).__name__} "
                f"exception occurred during unpack operation, "
                f"dump above shows interrupted progress, original "
                f"exception traceback appears above this exception's "
                f"traceback"
            ).with_traceback(exc.__traceback__)

        return item, dump.get_table()

    def unpack(self, cls):
        """Unpack item from memory bytes.

        :param type cls: item class
        :returns: item
        :rtype: cls

        """
        consumed = self.consumed
        try:
            return cls.__unpack__(self, None, None)

        except Exception:
            # do it over to include dump in exception message
            self.consumed = consumed
            self.unpack_and_getdump(cls)
            raise ImplementationError()

    def consume_bytes(self, nbytes, dump=None, cls=None):
        """Get memory bytes and advance consumed index.

        :param int nbytes: bytes to consume
        :param Dump dump: memory summary dump
        :param type cls: plum type of item that consumed bytes are for
        :returns: memory bytes
        :rtype: memoryview

        """
        end = self.consumed + nbytes

        # this might go beyond artificial limit, but it'll get caught
        buffer = self.buffer[self.consumed:end]

        try:
            dump.cls = cls
            dump.memory = buffer
        except AttributeError:
            pass  # dump is None

        if end > self.nbytes:
            try:
                dump.value = '<insufficient bytes>'
                # recalculate to only include those before any artificial limit
                dump.buffer = self.buffer[self.consumed:self.nbytes]
            except AttributeError:
                pass  # dump is None

            cls_name = '' if cls is None else f'{cls.__name__} '

            unpack_shortage = (
                f'{end - self.nbytes} too few memory bytes to unpack {cls_name}'
                f'({nbytes} needed, only {self.available} available)')

            raise InsufficientMemoryError(unpack_shortage)

        self.consumed = end

        return buffer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            buffer = self.buffer
            nbytes = len(buffer)
            if self.consumed != nbytes:
                msg = (
                    f'{nbytes - self.consumed} unconsumed memory bytes '
                    f'({nbytes} available, '
                    f'{self.consumed} consumed)'
                )
                extra_bytes = buffer[self.consumed:]
                raise ExcessMemoryError(msg, self.consumed, extra_bytes)
