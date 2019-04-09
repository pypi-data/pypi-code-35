__version__ = '0.1.0'

LOGGER_ROOT = 'dophon_logger.'

COMMAND = {
    'name': 'command'
}

DOPHON = {
    'name': 'dophon',
}

HUES = {
    'name': 'hues',
}

# 日志部件缓存(单例)
logger_cache = {}


class LogCell:

    def inject_logger(self, globals):
        pass

    def info(self, msg):
        pass

    def error(self, msg):
        pass

    def debug(self, msg):
        pass

    def warn(self, msg):
        pass

    def warning(self, msg):
        pass


def get_logger(logger_type: dict) -> LogCell:
    if logger_type['name'] in logger_cache:
        # 初始化过日志组件则直接返回
        return logger_cache[logger_type['name']]
    if logger_type != COMMAND:
        try:
            logger = __import__(LOGGER_ROOT + logger_type['name'], fromlist=True)
            cache_type = logger_type['name']
        except Exception as e:
            print('无法获取的日志配置:', e)
            # 获取日志配置失败则返回默认配置
            logger = __import__(LOGGER_ROOT + COMMAND['name'], fromlist=True)
            cache_type = logger_type['name']
    else:
        logger = __import__(LOGGER_ROOT + logger_type['name'], fromlist=True)
        cache_type = logger_type['name']
    # 缓存日志组件
    logger_cache[cache_type] = logger
    return logger
