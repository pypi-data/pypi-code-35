#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'iter'
__author__ = 'JieYuan'
__mtime__ = '18-12-14'
"""

from .utils.xx import xx
from .eda import DataFrameSummary
from .utils import cprint

try:
    from IPython import get_ipython

    if 'IPKernelApp' not in get_ipython().config:
        raise ImportError("console")
except:
    from tqdm import tqdm

else:
    from tqdm import tqdm_notebook as tqdm

#########################################################################
import warnings

warnings.filterwarnings("ignore")
import jieba
import json
import pickle
import numpy as np
import pandas as pd
from functools import reduce
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from sklearn.feature_extraction.text import TfidfVectorizer

# pd.set_option('display.max_rows', 1024)
# pd.set_option('display.max_columns', 128)
# pd.set_option('max_colwidth', 128)  # 列宽
# pd.set_option('expand_frame_repr', False)  # 允许换行显示


import matplotlib.pyplot as plt

# plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['Simhei']  # 中文乱码的处理
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 负号
plt.rcParams["text.usetex"] = False
plt.rcParams["legend.numpoints"] = 1
plt.rcParams["figure.figsize"] = (12, 6)  # (8, 6)
plt.rcParams["figure.dpi"] = 128
plt.rcParams["savefig.dpi"] = plt.rcParams["figure.dpi"]
plt.rcParams["font.size"] = 10
plt.rcParams["pdf.fonttype"] = 42

import seaborn as sns

sns.set(style="darkgrid")  # darkgrid, whitegrid, dark, white,和ticks

# sns.plotting_context()
# sns.axes_style()
#########################################################################
TfidfVectorizer


# 序列化
# df.to_hdf('./data.h5', 'w', complib='blosc', complevel=8)
def reader(fname='./tmp.txt', sep=',', mode='r'):
    with open(fname, mode) as f:
        for l in f:
            yield l.strip().split(sep)


@xx
def xwrite(iterable, fname, mode='w', glue='\n'):
    with open(fname, mode) as f:
        for item in iterable:
            f.write(str(item) + glue)


@xx
def xpickle_dump(obj, file='tmp.pkl'):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)


@xx
def xpickle_load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


# 统计函数: 待补充groupby.agg
xsummary = xx(lambda iterable: DataFrameSummary(list(iterable) | xDataframe)['iterable'])
xvalue_counts = xx(
    lambda iterable, normalize=False, bins=None: pd.value_counts(list(iterable), normalize=normalize, bins=bins))

__funcs = [sum, min, max, abs, len, np.mean, np.median]
xsum, xmin, xmax, xabs, xlen, xmean, xmedian = [xx(i) for i in __funcs]

xnorm = xx(lambda iterable, ord=2: np.linalg.norm(list(iterable), ord))
xcount = xx(lambda iterable: Counter(list(iterable)))

xunique = xx(lambda iterable: list(OrderedDict.fromkeys(list(iterable))))  # 移除列表中的重复元素(保持有序)
xsort = xx(lambda iterable, reverse=False, key=None: sorted(list(iterable), key=key, reverse=reverse))

xmax_index = xx(lambda x: max(range(len(x)), key=x.__getitem__))  # 列表中最小和最大值的索引
xmin_index = xx(lambda x: min(range(len(x)), key=x.__getitem__))  # 列表中最小和最大值的索引
xmost_freq = xx(lambda x: max(set(x), key=x.count))  # 查找列表中频率最高的值, key作用于set(x), 可类推出其他用法

# print
xprint = xx(lambda obj, bg='blue': cprint(obj, bg))
xtqdm = xx(lambda iterable, desc=None: tqdm(iterable, desc))

# base types
xtuple, xlist, xset = xx(tuple), xx(list), xx(set)

# string
xjoin = xx(lambda string, sep=' ': sep.join(string))
xcut = xx(lambda string, cut_all=False: jieba.cut(string, cut_all=cut_all))

# list transform
xgroup_by_step = xx(lambda ls, step=3: [ls[idx: idx + step] for idx in range(0, len(ls), step)])


# dict
@xx
def xjson(dict_):
    _ = json.dumps(dict_, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
    return _


@xx
def xSeries(iterable, name='iterable'):
    if isinstance(iterable, pd.Series):
        return iterable
    else:
        return pd.Series(iterable, name=name)


@xx
def xDataframe(iterable, name='iterable'):
    if isinstance(iterable, pd.DataFrame):
        return iterable
    else:
        return pd.DataFrame({name: iterable})


# 高阶函数
xmap = xx(lambda iterable, func: map(func, iterable))
xreduce = xx(lambda iterable, func: reduce(func, iterable))
xfilter = xx(lambda iterable, func: filter(func, iterable))


# multiple
@xx
def xThreadPoolExecutor(iterable, func, max_workers=5):
    with ThreadPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


@xx
def xProcessPoolExecutor(iterable, func, max_workers=5):
    with ProcessPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


import jovian


def jupyter_commit(filename=None):
    print(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlkZW50aXR5Ijp7InVzZXJuYW1lIjoiSmllLVl1YW4iLCJpZCI6Njd9LCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUyOTY1NTkzLCJpYXQiOjE1NTIzNjA3OTMsIm5iZiI6MTU1MjM2MDc5MywianRpIjoiNjM1ZTg2MjQtYjA1ZC00NGJmLTljYjAtOGVjOGRmM2ExNmJkIn0.5jglhEGGs12ITl-DWWaFL-BVPhCzaDEeMKIJvEI-bbA")
    print('\n')
    jovian.commit(filename=filename, env_type='pip')
