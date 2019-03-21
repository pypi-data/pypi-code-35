# coding=utf-8

__author__ = 'songmengyun'

from python_decorate.function_decorate import *

# 函数装饰器调用
@use_logging
def bar():
    print("i am bar")
bar()

@use_logging1(level="warn")
def foo(name='foo'):
    print("i am %s" % name)
foo()

@logged
def f(x):
    """does some math"""
    return x + x * x
print (f.__name__)  # prints 'f'
print (f.__doc__)


# 类装饰器调用
@Foo
def bar_class():
    print ('bar_class')
bar_class()




