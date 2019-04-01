# pylint: disable=no-self-use,invalid-name
import pytest

import funcsubs

TEST_HOOK = []


class C1:

    sync_pre_hook = funcsubs.SyncSideEffectSignal()
    async_pre_hook = funcsubs.AsyncSideEffectSignal()
    t1 = True

    def test1(self):
        self.sync_pre_hook.dispatch(self.__class__)
        print('5')

    async def test2(self):
        await self.async_pre_hook.dispatch(self.__class__)
        print('5')


class C2(C1):

    t1 = False


class Z1:

    sync_pre_hook = funcsubs.SyncInplaceEffectSignal()
    async_pre_hook = funcsubs.AsyncInplaceEffectSignal()
    t1 = True

    def test1(self):
        self.sync_pre_hook.dispatch(self.__class__)
        print('5')

    async def test2(self):
        await self.async_pre_hook.dispatch(self.__class__)
        print('5')


class Z2(Z1):

    t1 = False


def simple_hook(*_args, **_kwargs):
    TEST_HOOK.append(0)


async def async_hook(*_args, **_kwargs):
    TEST_HOOK.append(1)


def test_base_sync_logic():
    C1.sync_pre_hook.add_callback(simple_hook, lambda x: not x.t1)
    TEST_HOOK.clear()
    C1().test1()
    assert TEST_HOOK == []
    C2().test1()
    assert TEST_HOOK == [0]
    C1.sync_pre_hook.clear()
    TEST_HOOK.clear()
    C2().test1()
    assert TEST_HOOK == []


@pytest.mark.asyncio
async def test_base_async_logic():
    C1.async_pre_hook.add_callback(simple_hook, lambda x: not x.t1)
    C1.async_pre_hook.add_callback(async_hook, lambda x: not x.t1)
    TEST_HOOK.clear()
    await C1().test2()
    assert TEST_HOOK == []
    await C2().test2()
    assert TEST_HOOK == [0, 1]
    C1.async_pre_hook.clear()
    TEST_HOOK.clear()
    C2().test1()
    assert TEST_HOOK == []


def test_inplace_sync_logic():
    Z1.sync_pre_hook.add_callback(simple_hook, lambda x: not x.t1)
    TEST_HOOK.clear()
    Z1().test1()
    assert TEST_HOOK == []
    Z2().test1()
    assert TEST_HOOK == [0]
    Z1.sync_pre_hook.clear()
    TEST_HOOK.clear()
    Z2().test1()
    assert TEST_HOOK == []


@pytest.mark.asyncio
async def test_inplace_async_logic():
    Z1.async_pre_hook.add_callback(simple_hook, lambda x: not x.t1)
    Z1.async_pre_hook.add_callback(async_hook, lambda x: not x.t1)
    TEST_HOOK.clear()
    await Z1().test2()
    assert TEST_HOOK == []
    await Z2().test2()
    assert TEST_HOOK == [0, 1]
    Z1.async_pre_hook.clear()
    TEST_HOOK.clear()
    Z2().test1()
    assert TEST_HOOK == []


def test_election():
    election_hook = funcsubs.SyncElectionSignal()
    election_hook.add_callback(lambda: ('a', 5))
    election_hook.add_callback(lambda: ('c', 7))
    election_hook.add_callback(lambda: ('b', 9))
    election_hook.add_callback(lambda: ('d', -1))
    assert election_hook.dispatch(None) == 'b'
