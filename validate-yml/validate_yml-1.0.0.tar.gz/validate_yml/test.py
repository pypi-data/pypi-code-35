# # -*- coding:utf-8 -*-
__author__ = 'jimmy'
__date__ = '2019/3/16'
import os
from functools import wraps
import pdb


def coroutine(func):
    """
    装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def start(*args, **kwargs):
        c = func(*args, **kwargs)
        next(c)
        return c
    return start


def recursive():
    f_p = None
    while True:
        path = yield
        if path is None:
            break
        if os.path.isdir(path):
            parents = os.listdir(path)
            for parent in parents:
                child = os.path.join(path, parent)
                if os.path.isdir(child):
                    pass
                elif os.path.isfile(child) and (path.endswith('.yml') or path.endswith('.yaml')):
                    f_p = path
        else:
            f_p = path
    return f_p


# 委派生生成器
@coroutine
def grouper():
    f_p = None
    # pdb.set_trace()
    while True:
        f_p = yield from recursive()
        print(f_p)
            # check_yml_syntax().send(f_p)


g = grouper()
g.send('aa')
g.send(None)

# from collections import namedtuple
#
#
# Result = namedtuple('Result', 'count average')
#
#
# # 子生成器
# def averager():
#     total = 0.0
#     count = 0
#     average = None
#     while True:
#         term = yield
#         if term is None:
#             break
#         total += term
#         count += 1
#         average = total/count
#     return Result(count, average)
#
#
# # 委派生成器
# def grouper(result, key):
#     while True:
#         result[key] = yield from averager()
#
#
# # 客户端代码，即调用方
# def main(data):
#     results = {}
#     for key,values in data.items():
#         group = grouper(results,key)
#         next(group)
#         for value in values:
#             group.send(value)
#         group.send(None) #这里表示要终止了
#
#     report(results)
#
#
# # 输出报告
# def report(results):
#     for key, result in sorted(results.items()):
#         group, unit = key.split(';')
#         print('{:2} {:5} averaging {:.2f}{}'.format(
#             result.count, group, result.average, unit
#         ))
#
# data = {
#     'girls;kg':
#         [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
#     'girls;m':
#         [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
#     'boys;kg':
#         [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
#     'boys;m':
#         [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
# }
#
#
# if __name__ == '__main__':
#     main(data)