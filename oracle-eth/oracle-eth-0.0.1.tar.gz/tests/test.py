#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from oracle.database.db import *


# def test():
#     logger.info("xxxxxxx")


if __name__ == "__main__":
    # test()
    # logger.info("my test.")
    # logger.error("my test.")
    # create_person(name='yuyongpeng')
    # query_person(name='cat')
    # key = query_keys('6bS8KmBtE1Rs5Eg')
    # logger.info(key.address)

    str1 = 'testing '
    str2 = 'string '
    str3 = 'concation '
    # str = ''.join([str1, str2, str3])
    # print(str)



class Generator(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("There's no way out")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
          # 检查退出的类型
        # 当有异常发生时 exc_type存在值
        if exc_type:
            print('Open the door')
        else:
            print('100%')

    def generate(self):
        print('%s can uses love to generate electricity' % self.name)

# 紧跟with后面的语句被求值后，返回对象的 `__enter__() `方法被调用,
# 这个方法的返回值将被赋值给as后面的变量
with Generator("LEX") as lex:
    lex.generate()
# 当with后面的代码块全部被执行完之后，将调用返回对象的 `__exit__()`方法。

from contextlib import contextmanager
@contextmanager
def opening(filename):
    f = open(filename)  # IOError is untouched by GeneratorContext
    try:
        yield f
    finally:
        f.close()  # Ditto for errors here (however unlikely)

class MyFunc(object):
    """实现上下文管理器"""

    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        self.f_obj = open(self.file_name, self.mode)
        return self.f_obj          # __enter__函数返回的是打开资源的对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f_obj.close()


with open("file_name", "r") as file_obj:
    content = file_obj.read()

print(content)