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
    Url: https://github.com/GitHuHao/effective_sql.git
    Version: 0.1.10
"""

import gevent
import pymysql, pymysql.cursors
from DBUtils.PooledDB import PooledDB
import time,traceback
import logging

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
                conn_retries=3
                conn_retry_sleep=3
                execute_retries=3
                settings=('SET names utf8',)
                loglevel='DEBUG|INFO|ERROR'
        '''
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.passwd = kwargs['passwd']
        self.db = kwargs['db']
        self.port = kwargs['port'] if 'port' in kwargs else 3306
        self.charset = kwargs['charset'] if 'charset' in kwargs else 'utf8'
        self.cursor_key = kwargs['cursor_type'] if 'cursor_type' in kwargs else 'DictCursor'
        self.cursor_type = CURSORS[self.cursor_key]
        self.conn_retries = kwargs['conn_retries'] if 'conn_retries' in kwargs else 3
        self.conn_retry_sleep = kwargs['conn_retry_sleep'] if 'conn_retry_sleep' in kwargs else 3
        self.execute_retries = kwargs['execute_retries'] if 'execute_retries' in kwargs else 3
        self.settings = ['SET names utf8', ]
        if 'settings' in kwargs:
            settings = kwargs['settings']
            if isinstance(settings, str):
                settings = [settings, ]
            self.settings.extend(settings)
        self.loglevel = kwargs['loglevel'] if 'loglevel' in kwargs else 'DEBUG'

        logging.basicConfig(
            format='%(asctime)s [line:%(lineno)3d] %(levelname)7s: %(message)s',
            level=getattr(logging, self.loglevel)
        )
        self.logger = logging

        self.conn = None

    def add_logger(self, logger):
        self.logger = logger
        return self

    def _conn(self, connect_timeout=60):
        self.logger.info('CREATE DB(%s) CONNECTION .' % self.db)

        # self.conn = pymysql.Connection(host=self.host, user=self.user, passwd=self.passwd,
        #                                db=self.db, port=self.port, charset=self.charset,
        #                                connect_timeout=connect_timeout)

        self.pool = PooledDB(creator=pymysql, mincached=5, host=self.host, user=self.user, passwd=self.passwd,
                             db=self.db, port=self.port, charset=self.charset, connect_timeout=connect_timeout)

        # 可共享
        self.conn = self.pool.connection(shareable=True)

        # self.logger.debug('SET AUTOCOMMIT FALSE;')
        # self.conn.autocommit(False)
        self.cursor = self.conn.cursor(self.cursor_type)
        for setting in self.settings:
            self.cursor.execute(setting)
            self.logger.warn(setting.upper())

    def _reConn(self):
        retry_cnt = 0
        while retry_cnt < self.conn_retries:
            try:
                if self.conn is None:
                    self._conn()
                self.conn.ping()
                break
            except:
                retry_cnt += 1
                self.logger.error('%s PING FAILED FOR [ %s ]\n SLEEP FOR %s s .' % (retry_cnt,
                    traceback.format_exc(0), self.conn_retry_sleep))
                time.sleep(self.conn_retry_sleep)
                self._conn()

    def _close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        self.logger.info('CURSOR & CONNECTION IS CLOSED .')

    def _atomic_action(self, sql, params, detail):
        retry_cnt = 0
        result = -1
        error = None
        while retry_cnt < self.execute_retries:
            try:
                self._reConn()
                result = self.cursor.executemany(sql, params)
                # (submits,total_submit, start, end, total_records)
                self.logger.debug('[%s/%s:(%s->%s)/%s]' % detail + ' %s time success .' % (retry_cnt + 1))
                self.conn.commit()
                error = None
                break
            except Exception as e:
                try:
                    self.conn.rollback()
                except:
                    self.logger.error('[%s/%s:(%s->%s)/%s]' % detail + 'rollback fail for %s.' % traceback.format_exc(0))
                result = 0
                retry_cnt += 1
                error = e
                self.logger.error('[%s/%s:(%s->%s)/%s]' % detail + ' %s time fail for %s.' % ((retry_cnt + 1),
                    traceback.format_exc(0)))

        if error is not None:
            raise error
        return result

    def _batch_action(self, sql, params, batch, pojo, optimized=True):
        '''
        self.cursor.execute("SET GLOBAL max_allowed_packet=1024*1024*1024")
        :param sql:
        :param params: tuple、multi-array、dict、dict-list
        :param batch:  single thread processing batch
        :return: the effected lines.
        '''
        idxes = [(i, i + batch) for i in range(0, len(params), batch)]
        total_records = len(params)
        total_submit = len(idxes)

        submits = 0

        result = []

        self.logger.debug("EXECUTE ON %s MODE ." % 'YIELD' if optimized else 'MAIN')
        for start, end in idxes:
            submits += 1
            end = min(end, total_records)
            detail = (submits, total_submit, start, end - 1, total_records)
            if not optimized:
                # # 单线程
                result.append(self._atomic_action(sql, params[start:end], detail))
            else:
                # # 协程
                result.append(gevent.spawn(self._atomic_action, sql, params[start:end], detail))
                gevent.joinall(result)

        result = sum(result) if not optimized else sum([future.get() for future in result])

        if self.is_select:
            result = self.cursor.fetchall()
            self.logger.debug("FETCH %s ROWS ." % len(result))
            if pojo is not None:
                if isinstance(result[0], dict):
                    result = [pojo(**res) for res in result]
                else:
                    result = [pojo(*res) for res in result]
                self.logger.debug("WRAPPER %s ROWS ." % len(result))

        return result

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

        self.logger.debug('%s\n%s' % (sql, params[:1] if len(params) > 20 else params if showargs else ''))

        success = False
        result = None
        try:
            self.is_select = sql.lstrip().lower().startswith("select")

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
            self._close()
            return (success, result)