# pylint: disable=no-self-use,invalid-name
import funcsubs


TEST_HOOK = []


def simple_hook(*_args, **_kwargs):
    TEST_HOOK.append(0)


def test_dict_passing():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

        test1.lalka = 'lalka'

    TEST_HOOK.clear()
    C1.pre_hook(C1.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 2
    assert TEST_HOOK[0] == 0
    assert TEST_HOOK[1] == 1
    assert C1.test1.lalka == 'lalka'
