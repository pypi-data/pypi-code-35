from hawkei.store import Store

def test_init_store():
    Store.init()

    assert Store.get() == {}

def test_store_add():
    Store.init()

    assert Store.get() == {}
    assert Store.add({'test': True}) == {'test': True}
    assert Store.get() == {'test': True}

def test_store_clear():
    Store.init()

    assert Store.add({'test': True}) == {'test': True}
    assert Store.clear() == {}
    assert Store.get() == {}

def test_store_delete():
    Store.init()
    Store.delete()

    try:
        Store._store.val
    except AttributeError:
        assert True
    else:
        assert False

def test_get_without_init_store():
    assert Store.get() == {}

def test_clear_without_init_store():
    assert Store.clear() == {}

def test_add_without_init_store():
    assert Store.add({'test': True}) == {}
