import time


# 将秒时间戳转化为格式时间
def time2str(timestamp):
    tl = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", tl)


# 获取 10 位时间戳，秒
def second():
    return int(time.time())


# 获取 13 位时间戳，毫秒
def millisecond():
    return int(time.time() * 1000)
