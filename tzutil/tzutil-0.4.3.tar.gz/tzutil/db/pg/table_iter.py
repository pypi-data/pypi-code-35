#!/usr/bin/env python

from tqdm import tqdm
tqdm.monitor_interval = 0

class Schema:
    def __init__(self, pg):
        self._pg = pg

    def __getattr__(self, schema):
        return Table(self._pg, schema)


class Table:
    def __init__(self, pg, schema):
        self._pg = pg
        self.schema = schema

    def __getattr__(self, name):
        return Iter(self._pg, self.schema + "." + name)


TABLE_ID_ITER = "table_id_iter"


class TableIdIter:
    def __init__(self, pg, table, tag):
        self._pg = pg
        self._table = table
        self._tag = tag
        self._query = {'"table"': self._table, "tag": self._tag}

    def __int__(self):
        pos = self._pg.select_one(
            TABLE_ID_ITER,
            self._query,
            "pos",
        ) or 0
        self._pos = pos.pos if pos else pos
        return self._pos

    def __lshift__(self, value):
        pos = getattr(self, "_pos", None)
        if pos is None:
            pos = int(self)
        d = dict(self._query)
        if not value:
            self._pg.delete(TABLE_ID_ITER, d)
            return
        if pos:
            self._pg.update(TABLE_ID_ITER, dict(pos=value), d)
        else:
            d["pos"] = value
            self._pg.insert(TABLE_ID_ITER, d, on_conflict='("table",tag) DO UPDATE SET pos=excluded.pos')
        self._pos = value


class Iter:
    def __init__(self, pg, table, tag=""):
        self._id = TableIdIter(pg, table, tag)

    @property
    def _key(self):
        _id = self._id
        return ".".join((_id._table, _id._tag))

    def __getattr__(self, tag):
        return Iter(self._id._pg, self._id._table, tag)

    def __call__(self, where={}):
        id = self._id
        table = id._table

        where['id__gt'] = int(id)
        pg = self._id._pg
        count = pg.count_one(table, where=where)
        if count:
            process = tqdm(range(count), unit="row")

            for i in pg.iter(table, where=where, order='id'):
                yield i
                process.update()
            id << i.id

    def __lshift__(self, value):
        self._id << value



if __name__ == "__main__":
    print(TABLE_ITER.x.b.test)
