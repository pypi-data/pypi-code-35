from .pgwrap import db, connection
from tzutil.ob import Ob

query = db.cursor.query


def _query(self, *args, **kwds):
    return [Ob(**i) for i in query(self, *args, **kwds)]


db.cursor.query = _query

query_one = db.cursor.query_one


def _query_one(self, *args, **kwds):
    r = query_one(self, *args, **kwds)
    if r:
        r = Ob(**r)
    return r


db.cursor.query_one = _query_one


def _select_id_in(self, table, id_list, column="*"):
    if not id_list:
        return ()
    return self.query(
        f"SELECT {column} FROM {table} WHERE id in (%s)" %
        (",".join(map(str, id_list)))
    )


db.cursor.select_id_in = _select_id_in


def _upsert_id(self, table, column, value):
    sql = f"""with s as (select id from {table} where "{column}"=%s),
i as (
insert into {table} ("{column}")
select %s where not exists (select 1 from s)
returning id
) select id from i union all select id from s"""
    r = self.query_one(sql, (value, value))
    return r['id']


db.cursor.upsert_id = _upsert_id


def _iter(self, table, where=0, **kwds):
    where = where or {}
    order = kwds.get('order', '').lower()

    if order:
        del kwds['order']
    else:
        order = 'id desc'

    if order == 'id':
        id = 0
        where_id = 'id__gt'
        id = where.get(where_id, 0)
    elif order == 'id desc':
        where_id = 'id__lt'
        id = where.get(where_id, 0)
        if not id:
            o = self.select_one(
                table, columns=('id', ), limit=1, order=(order, )
            )
            if not o:
                return []
            id = o['id'] + 1
    else:
        raise

    if 'limit' not in kwds:
        kwds['limit'] = 1000

    while True:

        where[where_id] = id
        li = self.select(table, order=(order, ), where=where, **kwds)
        if li:
            for i in li:
                yield i
            id = i['id']
        else:
            break


connection.iter = _iter

if __name__ == "__main__":
    from .config import PSQL

    pg = connection(
        "postgres://%s:%s@%s:%s/%s" %
        (PSQL.USER, PSQL.PASSWORD, PSQL.HOST, PSQL.PORT, PSQL.DB)
    )

    for i in pg.iter("mail"):
        print(i)
