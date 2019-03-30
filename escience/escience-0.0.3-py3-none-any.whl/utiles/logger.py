# encoding: utf-8
"""
@version: python3.6
@author: ‘eric‘
@license: Apache Licence 
@contact: steinven@qq.com
@site: 
@software: PyCharm
@file: logger.py
@time: 2019/3/28 21:49
"""
import logging


def logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    # 创建一个logger
    logger = logging.getLogger('escience')
    logger.setLevel(logging.INFO)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('log.txt',encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    fh.setFormatter(formatter,)
    ch.setFormatter(formatter)

    # 给logger添加handler
    if not logger.handlers:
        logger.addHandler(fh)
    return logger

if __name__ == '__main__':
    logger().info("info")
    logger().debug("debug")
    logger().warning("warning")
    logger().error("error")