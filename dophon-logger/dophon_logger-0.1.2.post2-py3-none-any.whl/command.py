import logging

# 设置默认的level为DEBUG
# 设置log的格式
logging.basicConfig(
    level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)


# 日志过滤非框架打印
class DefFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith('dophon')


def inject_logger(g: dict, var_name: str = 'logger'):
    logger = logging.getLogger(g['__name__'])
    logger.addFilter(DefFilter())
    g[var_name] = logger
