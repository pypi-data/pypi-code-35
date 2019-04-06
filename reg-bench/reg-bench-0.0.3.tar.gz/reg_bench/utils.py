def make_register(dct):
    def register(arity, *tags):
        def inner(func):
            dct[func] = {"arity": arity, "tags": tags, "name": func.__name__}
            return func

        return inner

    return register
