import cython


def f(a):
    return cython.inline("return a", a=a, force=True)


print(f(5))