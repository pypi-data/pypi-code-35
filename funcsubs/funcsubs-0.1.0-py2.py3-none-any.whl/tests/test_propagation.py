# pylint: disable=no-self-use,invalid-name
import funcsubs

TEST_HOOK = []


def simple_hook(*_args, **_kwargs):
    TEST_HOOK.append(0)


def simple_hook_5(*_args, **_kwargs):
    TEST_HOOK.append(5)


def simple_hook_7(*_args, **_kwargs):
    TEST_HOOK.append(7)


def test_base_propagation():
    class C1(funcsubs.SubscribableMixin):

        t1 = True
        t2 = True
        t3 = True

        def test1(self):
            TEST_HOOK.append(1)

    class C2(C1):

        t1 = False

    class C3(C1):

        t2 = False

    C1.pre_hook(C1.test1, simple_hook, lambda x: x.t1)
    C1.pre_hook(C1.test1, simple_hook_5, lambda x: x.t2)
    C1.pre_hook(C1.test1, simple_hook_7, lambda x: x.t3)

    TEST_HOOK.clear()

    C1().test1()
    assert len(TEST_HOOK) == 4
    assert TEST_HOOK == [0, 5, 7, 1]

    TEST_HOOK.clear()

    C2().test1()
    assert len(TEST_HOOK) == 3
    assert TEST_HOOK == [5, 7, 1]

    TEST_HOOK.clear()

    C3().test1()
    assert len(TEST_HOOK) == 3
    assert TEST_HOOK == [0, 7, 1]
