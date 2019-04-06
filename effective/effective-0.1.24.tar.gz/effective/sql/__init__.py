#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File Name: __init__.py
    Author: HuHao
    Mail: whohow20094702@163.com
    Created Time:  '2019/2/28 20:48:00'
    Info: A effective style to operate sql
          Support for HA-connection, retry-support, high-tolerance params, self-batch execution
    Licence: GPL Licence
    Url: https://github.com/GitHuHao/effective.git
    Version: 0.1.10
"""
import sys

import gevent
import pymysql, pymysql.cursors
from DBUtils.PooledDB import PooledDB
import time, traceback
import logging

version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib
    importlib.reload(sys)

CURSORS = {
    # ((100L, u'A100', 2500L),) 返回元组，游标存储在客户端
    "Cursor": pymysql.cursors.Cursor,
    # ((100L, u'A100', 2500L),) 返回元组，游标存储在服务端
    "SSCursor": pymysql.cursors.SSCursor,
    # ({'price': 2500L, 'id': 100L, 'name': u'A100'},) 返回字典，游标存储在客户端
    "DictCursor": pymysql.cursors.DictCursor,
    # ({'price': 2500L, 'id': 100L, 'name': u'A100'},) 返回字典，游标存储在服务端
    "SSDictCursor": pymysql.cursors.SSDictCursor
}

class MySQL:

    def __init__(self, kwargs=None):
        '''
        :param kwargs:
            mondary: host, user, passwd, db, port, charset
            potational:
                connect_timeout=60s,
                cursor_type (eg:Cursor\SSCursor\DictCursor\SSDictCursor)
                execute_retries 查询重试次数 3
                fail_sleep 重刷间隔 3
                settings=('SET names utf8',)
                setsession=self.settings,  # SET 配置操作集合，诸如：["set datestyle to ...", "set time zone ...","set autocommit 0","set name UTF-8"],
                mincached=1,  # 启动时，最小缓存连接数
                maxcached=2,   # 启动时，最大缓存连接数
                maxconnections=2,  # 最大允许连接数
                maxshared=0,   # 最大可共享连接数(0 不允许共享)
                maxusage=0,   # 每个链接最大重复使用次数(超过此次数回炉重造) 0: 一直使用
                reset=True,    # 归还连接时是否重置：False/None 时，当事务是以begin()开始时，执行rollback操作；为True时始终执行回滚
                blocking=True,     # 达到最大连接数时，是阻塞等待(True)还是报错退出(False)
                failures=pymysql.MySQLError,    # 自动考虑重试连接的异常
                ping=4     # 0 = None = never, 1 = default = whenever fetched from the pool, 2 = when a cursor is created, 4 = when a query is executed, 7 = always, and all other bit combinations of these values
                loglevel='DEBUG|INFO|ERROR'
        '''
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 3306)
        self.user = kwargs.get('user', 'root')
        self.passwd = kwargs.get('passwd', 'root')
        self.db = kwargs.get('db', 'test')
        self.charset = kwargs.get('charset', 'utf8')
        self.cursor_key = kwargs.get('cursor_type', 'DictCursor')
        self.cursor_type = CURSORS[self.cursor_key]
        self.execute_retries = kwargs.get('execute_retries', 3)
        self.fail_sleep = kwargs.get('fail_sleep', 3)
        defaults = ['SET names utf8;', ]
        settings = kwargs.get('settings', [])
        defaults.extend(settings)
        self.setsession = defaults
        self.mincached = kwargs.get('mincached', 1)
        self.maxcached = kwargs.get('maxcached', 2)
        self.maxconnections = kwargs.get('maxconnections', 2)
        self.maxshared = kwargs.get('maxshared', 0)
        self.maxusage = kwargs.get('maxusage', 0)
        self.reset = kwargs.get('reset', True)
        self.blocking = kwargs.get('blocking', True)
        self.failures = kwargs.get('failures', None)
        self.ping = kwargs.get('ping', 4)
        self.loglevel = kwargs.get('loglevel', 'DEBUG')
        self._pool_init()

        logging.basicConfig(
            format='%(asctime)s [line:%(lineno)3d] %(levelname)7s: %(message)s',
            level=getattr(logging, self.loglevel)
        )
        self.logger = logging
        self.logger.info('Init PooledDB(%s)' % self.db)

    def add_logger(self, logger):
        self.logger = logger
        return self

    def _pool_init(self):
        self.pool = PooledDB(
            pymysql
            , host=self.host
            , user=self.user
            , passwd=self.passwd
            , db=self.db
            , port=self.port
            , charset=self.charset
            , mincached=self.mincached
            , maxcached=self.maxcached
            , maxconnections=self.maxconnections
            , maxshared=self.maxshared
            , maxusage=self.maxusage
            , reset=self.reset
            , blocking=self.blocking
            , setsession=self.setsession
            , failures=self.failures
            , ping=self.ping
        )

    def _close(self, cursor, conn):
        '''
        归还连接
        :param cursor:
        :param conn:
        :return:
        '''
        cursor_close, conn_close = ('FAIL', 'FAIL')
        if cursor is not None:
            cursor.close()
            cursor_close = 'Success'
        if conn is not None:
            conn.close()
            conn_close = 'Success'
        self.logger.info('Close cursor(%s) then return connections(%s) to pool.' % (cursor_close, conn_close))

    def close(self):
        '''
        关闭连接池
        :return:
        '''
        self.pool.close()
        self.logger.info('Close all connections in pool(%s).' % self.db)

    def _atomic_action(self, sql, params, detail):
        retry_cnt = 0
        result = -1
        conn = None
        cursor = None
        records = '[%s/%s:(%s->%s)/%s]' % detail
        while retry_cnt < self.execute_retries:
            try:
                # SteadyDBConnection
                conn = self.pool.connection(shareable=False)
                conn.rollback()
                cursor = conn.cursor(self.cursor_type)
                result = cursor.executemany(sql, params)
                if sql.lstrip().lower().startswith("select"):
                    result = cursor.fetchall()
                conn.commit()
                self.logger.debug(records + ' %s time success .' % (retry_cnt + 1))
                break
            except Exception as e:
                conn.rollback()
                result = 0
                retry_cnt += 1
                self.logger.error(
                    records + ' %s time fail for %s. Sleep for %s seconds then retry.' % (
                        retry_cnt, traceback.format_exc(0), self.fail_sleep
                    )
                )
                time.sleep(self.fail_sleep)
                if retry_cnt == self.execute_retries:
                    raise e
            finally:
                self._close(cursor, conn)
        return result

    def _batch_action(self, sql, params, batch, pojo, optimized=True):
        '''
        self.cursor.execute("SET GLOBAL max_allowed_packet=1024*1024*1024")
        :param sql:
        :param params: tuple、multi-array、dict、dict-list
        :param batch:  single thread processing batch
        :return: the effected lines.
        '''
        is_select = sql.lstrip().lower().startswith("select")

        idxes = [(i, i + batch) for i in range(0, len(params), batch)]
        total_records = len(params)
        total_submit = len(idxes)

        submits = 0
        futures = []
        self.logger.debug("EXECUTE ON %s MODE ." % 'YIELD' if optimized else 'MAIN')
        for start, end in idxes:
            submits += 1
            end = min(end, total_records)
            detail = (submits, total_submit, start, end - 1, total_records)
            if not optimized:
                res, cursor = self._atomic_action(sql, params[start:end], detail)
                futures.append(res)
            else:
                futures.append(gevent.spawn(self._atomic_action, sql, params[start:end], detail))
                gevent.joinall(futures)

        result = [] if is_select else None
        if is_select:
            for future in futures:
                result.extend(future.get() if optimized else future)
            self.logger.debug("FETCH %s ROWS ." % len(result))

            if pojo is not None:
                if isinstance(result[0], dict):
                    result = [pojo(**res) for res in result]
                else:
                    result = [pojo(*res) for res in result]
                self.logger.debug("WRAPPER %s ROWS ." % len(result))
        else:
            result = sum([(future.get() if optimized else future) for future in futures])

        return result

    def fly(self,
            sql,  # crud 、 upsert sql or dataframe
            params=None,  # tuple、multi-array、pojo-list、dict、dict-list、Nothing
            pojo=None,  # pojo class
            fields=None,  # fields name of pojo which will be use
            batch=1024,  # single thread batch
            propagation=True,
            showargs=True
            ):
        '''
        :param sql:
            my.fly('select * from car where id=100')
            my.fly('select * from car where id=%s',params=(100L,))
            my.fly('select * from car where id=%(id)s', param_dict={'id':100L})
            my.fly('insert into car(price,id,name) values (%s,%s,%s)',params=(2500L,100L,'A100'))
        :param params: 元祖
        :param param_dict: 字典
        :param option: 操作 SqlOption.Query、SqlOption.Execute
        :param propagate: 是否抛出异常
        :return: (成功与否,影响行数 或 抓取数据集)
        '''

        sqlinfo = ('%s\n%s' % (sql, params[:1] if len(params) > 20 else params if showargs else '')).decode('utf-8')
        self.logger.debug(sqlinfo)

        success = False
        result = None
        try:
            # rebuild params for cursor.executemany func
            if params is None:
                params = ((),)
            elif type(params) not in (tuple, set, list):
                if isinstance(params, dict):
                    params = (params,)
                else:
                    params = ((params,),)
            elif type(params) in (tuple, set, list) and type(params[0]) not in (
                    tuple, set, list, dict) and fields is None:
                params = (params,)

            # parse pojo class and fields value
            if type(params[0]) not in (dict, tuple):
                pojo = type(params[0])
                if type(fields) not in (set, list, tuple):
                    fields = (fields,)
                params = [[getattr(param, field) for field in fields] for param in params]

            result = self._batch_action(sql, params, batch, pojo)
            success = True
        except Exception as e:
            if propagation:
                raise e
        finally:
            return (success, result)

    def api(self):
        self.usage = '''
        You can call like these :
        注意：插入语句如果带主键，主键自增，会导出冲突问题）
        1) CRUD 传参兼容 
            # query 直接传单参
            status,result =my.fly('select * from car where name="A100"')
            print(status,result)

            query 直接传单参
            print(my.fly('select * from car where price>1900'))
            print(status,result)

            # query 错误传参 兼容值 （顺便封装对象）
            status,result = my.fly('select name,price,id from car where name=%s',params="A100",pojo=Car)
            print(status,result)

            # query 错误传参 兼容 dict（顺便封装对象）
            status,result = my.fly('select price,id,name from car where name=%(name)s',params={'name':'A100'},pojo=Car)
            print(status,result)

            # query 错误传参 兼容 ('A100',) 和 ('A100') （顺便封装对象）
            status,result = my.fly('select price,id,name from car where name=%s',params=('A100',),pojo=Car)
            print(status,result)

        2）BATCH EXECUTE
            # execute insert update select delete （顺便封装对象）
            print(my.fly('insert into car(price,name) values (%s,%s)',params=(2500L,'A100')))
            print(my.fly('update car set price=%s where name=%s and price=%s', params=(1000,'A100',2500L)))
            print(my.fly('select price,id,name from car where name=%(name)s', params={'name': 'A100'}, pojo=Car)[1])
            print(my.fly('delete from car where name=%s',params='A100'))
            print(my.fly('select price,id,name from car where name=%(name)s', params={'name': 'A100'}, pojo=Car))

            # batch tuple insert
            params = [('A%s' % i, i) for i in range(1,1000000)]
            status, count = my.fly(sql='insert into car(name,price) values (%s,%s)', params=params)
            print(status, count)

            # batch dict insert
            param_dict = [{'id': i, 'name': 'A%s' % i, 'price': i} for i in range(1, 10000)]
            status, count = my.fly(sql='insert into car(name,price) values (%(name)s,%(price)s)', params=param_dict)
            print(status, count)

            # batch instance insert
            instances = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 100000)]
            rows = my.fly(sql='insert into car(name,price) values (%s,%s)', params=instances, fields=['name','price'])
            print(rows)

            # batch instance delete 兼容 fields 异常传参
            instances = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 2000)]
            rows = my.fly(sql='delete from car where name =%s', params=instances, fields='name')
            print(rows)

            # batch instance upsert
            instances = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 4000)]
            rows = my.fly(sql='INSERT INTO car(name,price) VALUES (%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name)',
                          params=instances, fields=['name', 'price'])
            print(rows)

        3)  BEST PRACTICE
            db.yaml
            -----------------------------------------------------------------------------
            # 数据库连接
            database:
              # 线上运行环境
              online:
                hybridb:
                  host: xxxxx
                  port: 3306
                  db: xxxx
                  user: xxxx
                  passwd: xxxx
                  cursor_type: DictCursor
                  loglevel: INFO

              # 线下编码环境
              offline:
                hybridb:
                  host: xxxxx
                  port: 3306
                  db: xxxxx
                  user: xxxxx
                  passwd: xxxxx
                  cursor_type: DictCursor
                  loglevel: DEBUG
            -----------------------------------------------------------------------------

            init.sql
            -----------------------------------------------------------------------------
            CREATE TABLE `car` (
              `id` int(3) NOT NULL AUTO_INCREMENT,
              `name` varchar(50) DEFAULT NULL,
              `price` bigint(5) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=2000 DEFAULT CHARSET=utf8;
            -----------------------------------------------------------------------------

            best-practice.py
            -----------------------------------------------------------------------------
            import sys,os
            from effective_sql import MySQL

            ENV = 'online' if sys.platform != 'darwin' else 'offline'

            class Car:
                def __init__(self,price,id,name):
                    self.price = price
                    self.id = id
                    self.name = name

                def __str__(self):
                    return 'Car: id=%s, price=%s, name=%s'%(self.id,self.price,self.name)

                def __repr__(self):
                    return 'Car: id=%s, price=%s, name=%s'%(self.id,self.price,self.name)

            def get_section(yml,*args):
                if os.path.exists(yml):
                    with open(yml, "r") as file:
                        config = yaml.load(file)
                    recursive = 0
                    while recursive < len(args):
                        config = config[args[recursive]]
                        recursive += 1
                    return config
                else:
                    raise RuntimeError("%s not exists"%yml)

            conf = get_section('db.yaml','database', ENV,'hybridb')
            client = MySQL(conf)

            cars = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 100000)]
            success,rows = client.fly(
                sql='INSERT INTO car(name,price) VALUES (%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name)',
                params=cars, fields=['name', 'price']
                )
            if success: print(rows)

            success,cars = client.fly(
                sql='select * from car where price>%s and price<%s',
                params=(1500,300),
                pojo=Car
            )
            if success: print(rows)
            -----------------------------------------------------------------------------

        End
        '''

        print(self.usage.replace('        ', '').decode('utf-8'))

        pass
