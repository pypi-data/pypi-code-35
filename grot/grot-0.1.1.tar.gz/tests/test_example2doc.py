from examples.example2doc import get_clean_function_source


def some_decorator(*_):
    def wrapper(fcn):
        return fcn

    return wrapper


@some_decorator('''
documentation text
can span multiple
lines and contain sample_function text
''', '''digraph {
	graph [fontname=helvetica nodesep=0.5 ranksep=0.5 sep=0.4]
	n_e [label="It is\neaiser" shape=tab]
}''')
def sample_function(arg_1, *args):
    """
        some body of that function named sample_function
    """
    _ = (arg_1,) + args
    _ = """
        different text
    """
    # example ends here
    _ = """
        and another
    """


def test_get_clean_function_source_1():
    assert get_clean_function_source(sample_function) == '''\
def sample_function(arg_1, *args):
    _ = (arg_1,) + args
    _ = """
        different text
    """

'''


@some_decorator('', '')
def sample_function2():
    pass
    pass


def test_get_clean_function_source_2():
    assert get_clean_function_source(sample_function2) == '''\
@some_decorator('', '')
def sample_function2():
    pass
    pass

'''


@some_decorator('', '')
def sample_function3():
    pass
    # example ends here
    pass


def test_get_clean_function_source_3():
    assert get_clean_function_source(sample_function3) == '''\
@some_decorator('', '')
def sample_function3():
    pass

'''


def undecorated(things):
    """
        Some docstring
    """
    things += 2
    return things


def test_get_clean_function_source_4():
    assert get_clean_function_source(undecorated) == '''\
def undecorated(things):
    things += 2
    return things

'''


def undecorated_with_terminator(things):
    """
        Some docstring
    """
    things += 2
    # example ends here
    return things


def test_get_clean_function_source_5():
    assert get_clean_function_source(undecorated_with_terminator) == '''\
def undecorated_with_terminator(things):
    things += 2

'''
