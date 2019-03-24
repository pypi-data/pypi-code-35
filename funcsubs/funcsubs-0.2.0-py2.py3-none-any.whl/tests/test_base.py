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
