import sqlite3, os, time, pickle
from .base import *
from .colorful_print import *
from .procedure import procedure
inf = 86400 * 365 * 1000

class DataBase(object):
    def __init__(self, path, tables=[], **kwargs):# {{{
        '''
            init of database
            restore path: path/name.db
        '''
        self._log_mode = 'cp'
        self._path = path
        with procedure('init database \'(#y){}(#)\''.format(self._path), False) as p:
            self.pack_dict = lambda keys, itemss:\
                    [{key: item for key, item in zip(keys, items)} for items in itemss]
            self._tables = tables
            self._conn = sqlite3.connect(self._path, check_same_thread=False)
            self._cursor = self._conn.cursor()
            self.db_initalize()
    # }}}
    def dump(self):# {{{
        self._conn.commit()
    # }}}
    def __del__(self):# {{{
        self._cursor.close()
        self._conn.commit()
        self._conn.close()
    # }}}
    def list_tables(self):# {{{
        tables = self.select('sqlite_master', keys='name',\
                limitation={'type': 'table'}, return_dict=False)
        return {table[0] for table in tables}
    # }}}
    def add_log(self, cmd, *args, limitation=200):# {{{
        if self._log_mode == 'cp':
            cp('(#g)SQL:(#) >> (#b){}'.format(
                (cmd + '    {}'.format(args))[:limitation]
            ))
    # }}}
    def execute(self, cmd, *args, dump=True):# {{{
        self.add_log(cmd, *args)
        ret = self._cursor.execute(cmd, *args)
        if dump:
            self.dump()
        return ret
    # }}}
    def add_tables(self, tables):# {{{
        if isinstance(tables, dict):
            tables = [tables]
        existed_tables = self.list_tables()
        for table in tables:
            if table['name'] in existed_tables:
                continue
            cmd = 'CREATE TABLE {} ({})'.format(
                table['name'],
                ', '.join([
                    '{} {}'.format(col['key'], col['db_type'])
                    for col in table['attr']
                ] + (table['extra'] if 'extra' in table else []))
            )
            self.execute(cmd, dump=True)
    # }}}
    def add_row(self, table_name, *, data):# {{{
        cmd = 'INSERT INTO {} ({}) VALUES ({})'.format(
            table_name, 
            ','.join(data.keys()),
            ('?,'*len(data.keys()))[:-1],
        )
        return self.execute(cmd, tuple(data.values()), dump=True)
    # }}}
    def add_rows(self, table_name, *, rows):# {{{
        data = rows[0]
        cmd = 'INSERT INTO {} ({}) VALUES {}'.format(
            table_name, 
            ','.join(data.keys()),
            ','.join(['({})'.format(
                ('?,'*len(data.keys()))[:-1],
            ) for data in rows])
        )
        values = []
        for data in rows:
            values += data.values()
        return self.execute(cmd, tuple(values), dump=True)
    # }}}
    def del_row(self, table_name, *, limitation=None):# {{{
        ''' 
        @params:
            limitation:
                1. str
                2. dict {key: value}
        '''
        values = tuple()
        if limitation is None:
            cmd = 'DELETE FROM {}'.format(table_name)
        elif isinstance(limitation, dict):
            cmd = 'DELETE FROM {} WHERE {}'.format(
                table_name,
                ' and '.join(['{}=?'.format(key) for key in limitation.keys()])
            )
            values += tuple(limitation.values())
        elif isinstance(limitation, str):
            cmd = 'DELETE FROM {} WHERE {}'.format(table_name, limitation)
        return self.execute(cmd, values, dump=True)
    # }}}
    def upd_row(self, table_name, *, data, limitation=None):# {{{
        ''' 
        @params:
            limitation & data:
                1. str
                2. dict {key: value}
        '''
        values = tuple(data.values())
        if limitation is None:
            cmd = 'UPDATE {} SET {}'.format(
                table_name,
                ', '.join(['{}=?'.format(key) for key in data.keys()]),
            )
        elif isinstance(limitation, dict):
            cmd = 'UPDATE {} SET {} WHERE {}'.format(
                table_name,
                ', '.join(['{}=?'.format(key) for key in data.keys()]),
                ' and '.join(['{}=?'.format(key) for key in limitation.keys()]),
            )
            values += tuple(limitation.values())
        elif isinstance(limitation, str):
            cmd = 'UPDATE {} SET {} WHERE {}'.format(
                table_name,
                ', '.join(['{}=?'.format(key) for key in data.keys()]),
                limitation,
            )
        return self.execute(cmd, values, dump=True)
    # }}}
    def select(self, table_name, *, extra='', limitation=None, keys='*', return_dict=True):# {{{
        ''' 
        @params:
            limitation:
                1. str
                2. return_dict {key: value}
            keys:
                1. *
                2. str
                3. list
        '''
        if limitation == {} or limitation == '':
            limitation = None
        if keys == '*':
            keys = [item[1] for item in self.execute(
                'PRAGMA table_info ({})'.format(table_name))]
        if isinstance(keys, str):
            keys = [keys]

        values = tuple()

        if limitation is None:
            cmd = 'SELECT {} FROM {}'.format(','.join(keys), table_name)
        elif isinstance(limitation, dict):
            cmd = 'SELECT {} FROM {} WHERE {}'.format(
                ','.join(keys),
                table_name,
                ' and '.join(['{}=?'.format(key) for key in limitation.keys()])
            )
            values += tuple(limitation.values())
        elif isinstance(limitation, str):
            cmd = 'SELECT {} FROM {} WHERE {}'.format(
                ','.join(keys),
                table_name,
                limitation,
            )
        cmd += ' ' + extra
        return self.pack_dict(keys, self.execute(cmd, values).fetchall()) if return_dict else\
                self.execute(cmd, values).fetchall()
    # }}}
    def count(self, table_name, *, limitation=None):# {{{
        ''' 
        @params:
            limitation:
                1. str
                2. return_dict {key: value}
        '''
        if limitation == {}:
            limitation = None

        values = tuple()

        if limitation is None or limitation == '':
            cmd = 'SELECT COUNT(*) FROM {}'.format(table_name)
        elif isinstance(limitation, dict):
            cmd = 'SELECT COUNT(*) FROM {} WHERE {}'.format(
                table_name,
                ' and '.join(['{}=?'.format(key) for key in limitation.keys()])
            )
            values += tuple(limitation.values())
        elif isinstance(limitation, str):
            cmd = 'SELECT COUNT(*) FROM {} WHERE {}'.format(
                table_name,
                limitation,
            )
        return self.execute(cmd, values).fetchall()[0][0]
    # }}}
    def get_global(self, name, default=None):# {{{
        data = self.select('global', limitation={'name': name})
        if len(data) > 0 and data[0]['duration'] > time.time():
            return pickle.loads(data[0]['value'])
        return default
    # }}}
    def vis_global(self, name):# {{{
        return self.count('global', limitation={'name': name}) == 1
    # }}}
    def set_global(self, name, data, expired_time=inf):# {{{
        if self.vis_global(name):
            self.upd_row('global', data={'value': pickle.dumps(data),\
                    'valid': time.time() + expired_time}, limitation={'name': name})
        else:
            self.add_row('global', data={'name': name, 'value': pickle.dumps(data),\
                    'valid': time.time() + expired_time})
    # }}}
    def drop_table(self, name):# {{{
        cmd = 'DROP TABLE {}'.format(name)
        return self.execute(cmd, dump=True)
    # }}}
    def db_initalize(self):# {{{
        self.add_tables(self._tables)
    # }}}

