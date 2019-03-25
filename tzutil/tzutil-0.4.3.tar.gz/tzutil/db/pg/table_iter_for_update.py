#!/usr/bin/env python

from time import time
from tqdm import tqdm
from random import shuffle, randint

DAY_SECONDS= 86400

def table_iter_for_update(pg, redis, R, table_iter, where={}, expire_day=1, next_time=None):
    key = R.TABLE.ITER.UPDATE.ZSET % table_iter._key
    #table_iter << 0

    if int(table_iter._id) == 0:
        redis.delete(key)

    for i in table_iter(where):
        redis.zadd(key, 0, i.id)

    now = int(time())
    li = redis.zrangebyscore(key, 0, now)

    # print(key)
    # shuffle(li)

    if next_time is None:
        expire_sec = expire_day*DAY_SECONDS

        def next_time(o):
            # 均衡化
            if expire_day > 1 and not redis.zscore(key, id):
                s = randint(1,expire_day)*DAY_SECONDS
            else:
                s = expire_sec
            return now + s

    for id in tqdm(li, unit="row"):
        o = pg.select_one(table_iter._id._table, dict(id=id))
        yield o


        redis.zadd(key, next_time(o), id)


