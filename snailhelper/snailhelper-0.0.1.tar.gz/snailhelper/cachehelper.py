# -*- conding: utf-8 -*-
"""数据共享助手"""
import time
import threading


def __init():
    """初始化"""
    global __lock
    global __cache

    __lock = threading.Lock()
    __cache = {
        '__GLOBAL__': {

        }
    }

    print('>>>>>> 初始化 [cachehelper.py] <<<<<<')


def get(key, default_val=None):
    """从缓存中获取数据"""
    try:
        __lock.acquire()
        return __cache['__GLOBAL__'][key][0]
    except KeyError:
        return default_val
    finally:
        __lock.release()


def get_local(key, default_val=None):
    """从当前线程中获取缓存数据"""
    try:

        mainkey = r'__LOCAL__%s' % threading.currentThread().getName()

        if __cache.get(mainkey) is None:
            return default_val

        return __cache[mainkey][key][0]
    except KeyError:
        return default_val


def put(key, value, timeout=1800):
    """放入缓存数据，默认保存时间30分钟"""

    timeout = time.time() + timeout
    data = [value, timeout]

    try:
        __lock.acquire()
        __cache['__GLOBAL__'][key] = data
    finally:
        __lock.release()

    mainkey = r'__LOCAL__%s' % threading.currentThread().getName()

    if __cache.get(mainkey) is None:
        __cache[mainkey] = {}

    __cache[mainkey][key] = data
    __cache[mainkey]['__CACHEHELPER_THREAD_CACHE_MAX_TIMEOUT__'] = timeout


def remove(key):
    """从缓存中移除数据"""
    try:
        __lock.acquire()
        __cache['__GLOBAL__'].pop(key)
    finally:
        __lock.release()

    mainkey = r'__LOCAL__%s' % threading.currentThread().getName()

    if __cache.get(mainkey):
        __cache[mainkey].pop(key)


def clear():
    __cache.clear()


def __monitoring():
    """定期清理过期数据"""
    while True:

        time.sleep(30)

        try:
            for k in __cache.keys():
                if '__GLOBAL__' == k:
                    gcache = __cache.get(k)

                    for k2 in gcache.keys():
                        data = gcache.get(k2)

                        if data and data[1] < time.time():
                            gcache.pop(k2)
                            print('清理过期数据：[%s, %s]' % (k2, data[0]))
                else:
                    tcache = __cache.get(k)

                    if tcache is None:
                        continue

                    timeout = tcache.get('__CACHEHELPER_THREAD_CACHE_MAX_TIMEOUT__')

                    if timeout and (time.time() > timeout):
                        __cache.pop(k)
                        print('清理过期[线程]数据：[%s, %s]' % (k, tcache))
        except:
            pass


# #################################### 初始化 ####################################
__init()


threading.Thread(
    target=__monitoring,
    name='定时清理cachehelper的缓存'
).start()
# ################################################################################




