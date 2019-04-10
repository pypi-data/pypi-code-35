# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import logging
from io import BytesIO

import pytest

from .. import (
    ExcessMemoryError,
    InsufficientMemoryError,
    SizeError,
    calcsize,
    getdump,
    pack,
    pack_and_getdump,
    unpack,
    unpack_from,
    unpack_and_getdump,
    unpack_from_and_getdump,
)

from .utils import wrap_message


def get_normalized_dump_str(dump):
    return str(dump).replace('| [0]', '| x  ')


class SampleType(type):

    def __new__(mcs, name, bases, namespace, validate=True):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, validate=True):
        super().__init__(name, bases, namespace)

        if validate:
            basecls = cls.__basecls__

            base_dir = {n for n in dir(basecls) if not n.startswith('_')}

            for name in {n for n in base_dir if not n.startswith('test')}:
                if (getattr(basecls, name) is ...) and (getattr(cls, name) is ...):
                    raise TypeError(f'subclass missing {name!r} attribute')

            cls_dir = {n for n in dir(cls) if not n.startswith('_')}

            extras = {n for n in cls_dir - base_dir if not n.startswith('test')}

            if extras:
                extras = list(sorted(extras))
                raise TypeError(f'illegal subclass attribute {extras}')
        else:
            # subclasses validate attributes against me
            cls.__basecls__ = cls


class Sample(metaclass=SampleType, validate=False):

    __basecls__ = None

    cls = ...
    """Plum type to test."""

    unpack_cls = None

    value = ...
    """Sample value to use to construct plum type instance and to compare."""

    def iter_instances(self):
        yield self.cls(self.value), "instantiated from self.value"

    def iter_values(self):
        yield self.value, "self.value"
        yield self.cls(self.value), "instance"


class BasicConformance(Sample, validate=False):

    """Test basic API conformance and utility usage."""

    bindata = ...
    """Sample packed binary data."""

    cls_nbytes = None
    """Size of plum type being tested."""

    dump = ...
    """Expected dump of sample plum type instance."""

    greedy = False
    """If plum type being tested consumes remaining memory."""

    pack = staticmethod(pack)
    """pack() function to test with (allow plum_c to override to recycle test cases)."""

    retval_str = None
    """Expected return value of __str__ method (default to str of value)."""

    retval_repr = None
    """Expected return value of __repr__ method (default to standard based on value)."""

    unpack = staticmethod(unpack)
    """unpack() function to test with (allow plum_c to override to recycle test cases)."""

    unpack_from = staticmethod(unpack_from)
    """unpack_from() function to test with (allow plum_c to override to recycle test cases)."""

    unpack_excess = ...
    """Expected exception message of unpack() method when 1 byte extra."""

    unpack_shortage = ...
    """Expected exception message of unpack() method when short 1 byte."""

    def test_init_via_value(self):
        """Test instantiation with single value."""
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert getdump(instance) == self.dump

    def test_calcsize_with_cls(self):
        if self.cls_nbytes is None:
            with pytest.raises(SizeError):
                calcsize(self.cls)
        else:
            assert calcsize(self.cls) == self.cls_nbytes

    def test_calcsize_with_instance(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert calcsize(instance) == len(self.bindata)

    def test_getdump(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert getdump(instance) == self.dump

    def test_pack_value(self):
        for value, desc in self.iter_values():
            logging.info(desc)
            assert self.pack(self.cls, self.value) == self.bindata

    def test_pack_and_getdump_value(self):
        for value, desc in self.iter_values():
            logging.info(desc)
            memory, dump = pack_and_getdump(self.cls, self.value)
            assert memory == self.bindata
            assert get_normalized_dump_str(dump) == self.dump

    def test_pack_instance(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert self.pack(instance) == self.bindata

    def test_pack_and_getdump_instance(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            memory, dump = pack_and_getdump(instance)
            assert memory == self.bindata
            assert get_normalized_dump_str(dump) == self.dump

    def test_unpack(self):
        item = self.unpack(self.cls, self.bindata)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value

    def test_unpack_from_default_start(self):
        if self.greedy:
            bindata = BytesIO(self.bindata)
        else:
            bindata = BytesIO(self.bindata + b'\x99')
        item = self.unpack_from(self.cls, bindata)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value

    def test_unpack_from_default_middle(self):
        if self.greedy:
            bindata = BytesIO(b'\x99' + self.bindata)
        else:
            bindata = BytesIO(b'\x99' + self.bindata + b'\x99')
        bindata.read(1)
        item = self.unpack_from(self.cls, bindata)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value

    def test_unpack_from_force_middle(self):
        if self.greedy:
            bindata = BytesIO(b'\x99' + self.bindata)
        else:
            bindata = BytesIO(b'\x99' + self.bindata + b'\x99')
        item = self.unpack_from(self.cls, bindata, offset=1)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value

    def test_unpack_and_getdump(self):
        item, dump = unpack_and_getdump(self.cls, self.bindata)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value
        assert dump == self.dump

    def test_unpack_from_and_getdump_default_start(self):
        if self.greedy:
            bindata = BytesIO(self.bindata)
        else:
            bindata = BytesIO(self.bindata + b'\x99')
        item, dump = unpack_from_and_getdump(self.cls, bindata)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value
        assert dump == self.dump

    def test_unpack_from_and_getdump_default_middle(self):
        if self.greedy:
            bindata = BytesIO(b'\x99' + self.bindata)
        else:
            bindata = BytesIO(b'\x99' + self.bindata + b'\x99')
        bindata.read(1)
        item, dump = unpack_from_and_getdump(self.cls, bindata)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value
        assert dump == self.dump

    def test_unpack_from_and_getdump_force_middle(self):
        if self.greedy:
            bindata = BytesIO(b'\x99' + self.bindata)
        else:
            bindata = BytesIO(b'\x99' + self.bindata + b'\x99')
        item, dump = unpack_from_and_getdump(self.cls, bindata, offset=1)
        expected_cls = self.unpack_cls or self.cls
        assert type(item) is expected_cls
        assert item == self.value
        assert dump == self.dump

    def test_unpack_shortage(self):
        if self.bindata:
            with pytest.raises(InsufficientMemoryError) as trap:
                self.unpack(self.cls, self.bindata[:-1])

            assert wrap_message(trap.value) == self.unpack_shortage

    # FUTURE - add shortage/excess for getdump versions

    def test_unpack_excess(self):
        if str(self.unpack_excess) != 'N/A':
            with pytest.raises(ExcessMemoryError) as trap:
                self.unpack(self.cls, self.bindata + b'\x99')

            assert wrap_message(trap.value) == self.unpack_excess

    def test_str(self):
        if self.retval_str is None:
            expected = str(self.value)
        else:
            expected = self.retval_str

        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert str(instance) == expected

    def test_repr(self):
        if self.retval_repr is None:
            expected = f'{self.cls.__name__}({self.value!r})'
        else:
            expected = self.retval_repr

        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert repr(instance) == expected
