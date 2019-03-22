# pylint: disable=no-self-use,invalid-name
import funcsubs


TEST_HOOK = []


def simple_hook(*_args, **_kwargs):
    TEST_HOOK.append(0)


def test_base_pre_hook():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    TEST_HOOK.clear()
    C1.pre_hook(C1.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 2
    assert TEST_HOOK[0] == 0
    assert TEST_HOOK[1] == 1


def test_double_pre_hook():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    TEST_HOOK.clear()
    C1.pre_hook(C1.test1, simple_hook)
    C1.pre_hook(C1.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 3
    assert TEST_HOOK == [0, 0, 1]


def test_inherit_pre_hook():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    class C2(C1):

        def test2(self):
            TEST_HOOK.append(2)
    TEST_HOOK.clear()
    C2.pre_hook(C2.test1, simple_hook)
    c2 = C2()
    c2.test1()
    assert len(TEST_HOOK) == 2
    assert TEST_HOOK[0] == 0
    assert TEST_HOOK[1] == 1


def test_inherit_pre_hook_ignore_case():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    class C2(C1):

        def test2(self):
            TEST_HOOK.append(2)
    TEST_HOOK.clear()
    C2.pre_hook(C2.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 1
    assert TEST_HOOK[0] == 1


def test_base_post_hook():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    TEST_HOOK.clear()
    C1.post_hook(C1.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 2
    assert TEST_HOOK[1] == 0
    assert TEST_HOOK[0] == 1


def test_double_post_hook():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    TEST_HOOK.clear()
    C1.post_hook(C1.test1, simple_hook)
    C1.post_hook(C1.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 3
    assert TEST_HOOK == [1, 0, 0]


def test_inherit_post_hook():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    class C2(C1):

        def test2(self):
            TEST_HOOK.append(2)
    TEST_HOOK.clear()
    C2.post_hook(C2.test1, simple_hook)
    c2 = C2()
    c2.test1()
    assert len(TEST_HOOK) == 2
    assert TEST_HOOK[1] == 0
    assert TEST_HOOK[0] == 1


def test_inherit_post_hook_ignore_case():
    class C1(funcsubs.SubscribableMixin):

        def test1(self):
            TEST_HOOK.append(1)

    class C2(C1):

        def test2(self):
            TEST_HOOK.append(2)
    TEST_HOOK.clear()
    C2.post_hook(C2.test1, simple_hook)
    c1 = C1()
    c1.test1()
    assert len(TEST_HOOK) == 1
    assert TEST_HOOK[0] == 1
