# -*- coding:utf-8 -*

import traceback
import time
import redis
from redis.sentinel import Sentinel

from log import logger
from singleton import singleton

hosts = '10.11.5.112:26380, 10.11.5.113:26380, 10.11.5.114:26380, 10.11.5.115:26380, 10.11.5.116:26380'
redis_name = 'redis_master'
redis_password = 'kdgogo'
db_list = 'ir_server,upload'
dblist = {'ir_server_db': 50, 'upload_db': 0}
@singleton
class Pool(object):
    def __init__(self):
        self.__get_sentinel()
        self.__create_redis()

    def __get_sentinel(self):
        sentinel_info = hosts
        sentinels = sentinel_info.split(',')
        sentinel_hosts = []
        for sentinel in sentinels:
            sentinel = sentinel.strip()
            host = sentinel.split(':')[0]
            port = int(sentinel.split(':')[1])
            sentinel_hosts.append((host, port))
        self.sentinel = Sentinel(sentinel_hosts, socket_timeout=15)

    def __create_redis(self):
        redis_name = redis_name
        redis_password = redis_password
        self.__redis_map = {}
        for db_name in db_list.split(','):
            db_name = db_name.strip()
            if not db_name:
                continue
            db_conf_name = db_name + '_db'
            db = dblist[db_conf_name]
            self.__redis_map[db_name] = RobustRedis(self.sentinel, redis_name, db=db,
                                                    redis_password=redis_password)

    def get(self, name):
        assert name in self.__redis_map, 'no redis for[%s]' % name
        return self.__redis_map[name] 

def make_robust(fun, obj, fun_name, recover):
    def new_fun(*args, **kw):
        arg = args
        f = fun
        for i in range(3):
            try:
                return f(*args, **kw)
            except Exception, e:
                logger().warning(traceback.format_exc())
                time.sleep(3)
                recover()
                f = getattr(obj, '__' + fun_name)
                continue
        raise Exception('Redis failed 3 times')
    return new_fun

class RobustRedis(object):
    def __init__(self, sentinel, redis_name, db, redis_password):
        self.__sentinel = sentinel
        self.__redis_name = redis_name
        self.__db = db
        self.__redis_password = redis_password
        self.migrate_robust_fun()

    def __get_master_from_sentinel(self):
        redis_name = self.__redis_name
        db = self.__db
        redis_password = self.__redis_password
        return self.__sentinel.master_for(redis_name, db=db,
                                          password=redis_password,
                                          socket_timeout=10)

    def migrate_robust_fun(self):
        master = self.__get_master_from_sentinel()
        for fun_name in dir(master):
            attr = getattr(master, fun_name)
            if fun_name == 'pipeline':
                setattr(self, fun_name, self.pipeline)
            else:
                if not fun_name.startswith('_'):
                    setattr(self, fun_name,
                            make_robust(attr, self, fun_name, self.recover))
                    setattr(self, '__' + fun_name, attr)

    def pipeline(self, *args, **kw):
        assert False, 'Not implemented'

    def recover(self):
        master = self.__get_master_from_sentinel()
        logger().info('switch master to [%s]', master)
        #self.migrate_robust_fun()

def get(name):
    pool = Pool()
    return pool.get(name)

def redis_pool_main():
    pool = Pool()
    r = pool.get('hbase_index_test')
    for i in range(1000):
        str_i = str(i)
        val = 'a+++' + str_i
        print r.set(str_i, val)

if __name__ == '__main__':
    #redis_pool_main()
    r = Pool().get('ir_server')
    r.set('test', '3')
    print r.get('test')
