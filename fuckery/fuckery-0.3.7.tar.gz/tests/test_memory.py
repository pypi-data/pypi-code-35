# -*- coding: utf-8 -*-
# XXX Update Docstring
"""
pyFuckery - test_memory.py
Created on 2/12/17.


"""
# Stdlib
import logging

# Third party code
import pytest

from fuckery import memory
# Custom code
from fuckery.exc import AddressError
from fuckery.exc import StorageError

# Logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s [%(filename)s:%(funcName)s]')
log = logging.getLogger(__name__)

TEST_MEMORY_SIZE = 100


@pytest.fixture()
def storage() -> memory.Storage:
    m = memory.Storage(n=TEST_MEMORY_SIZE)
    return m


class TestMemory:
    # noinspection PyShadowingNames
    def test_memory_initialize(self, storage: memory.Storage):
        assert isinstance(storage, memory.Storage) is True
        for i in range(TEST_MEMORY_SIZE):
            v = storage.get(i)
            assert v == 0

    # noinspection PyShadowingNames
    def test_memory_updating(self, storage: memory.Storage):
        addr = 10
        v = 20
        storage.set(addr=addr, value=v)
        r = storage.get(addr=addr)
        assert r == v
        # Do value bounds checking for acceptablbe values
        v = 0
        storage.set(addr=addr, value=v)
        r = storage.get(addr=addr)
        assert r == v
        v = 255
        storage.set(addr=addr, value=v)
        r = storage.get(addr=addr)
        assert r == v

    # noinspection PyShadowingNames
    def test_magic_methods(self, storage: memory.Storage):
        addr = 10
        assert 0 in storage
        assert addr in storage
        assert TEST_MEMORY_SIZE-1 in storage
        assert TEST_MEMORY_SIZE not in storage
        addr = 10000
        assert addr not in storage

        assert len(storage) == TEST_MEMORY_SIZE

    # noinspection PyShadowingNames
    def test_bad_inputs(self, storage: memory.Storage):
        with pytest.raises(AddressError) as cm:
            storage.get(1000)
        assert 'Address is invalid' in str(cm.value)

        with pytest.raises(AddressError) as cm:
            storage.set(1000, 0)
        assert 'Address is invalid' in str(cm.value)

        with pytest.raises(StorageError) as cm:
            storage.set(0, '0x00')
        assert 'Value is not an int' in str(cm.value)

        with pytest.raises(StorageError) as cm:
            storage.set(0, 0.0)
        assert 'Value is not an int' in str(cm.value)

        with pytest.raises(StorageError) as cm:
            storage.set(0, -1)
        assert 'Value is out of size bounds' in str(cm.value)

        with pytest.raises(StorageError) as cm:
            storage.set(0, 256)
        assert 'Value is out of size bounds' in str(cm.value)
