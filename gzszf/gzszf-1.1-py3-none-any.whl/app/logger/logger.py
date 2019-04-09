# -*- coding: utf-8 -*- 
# @Time : 2019/4/8 13:38 
# @Author : Allen 
# @Site :  日志模块
import logging
import datetime


class Log:
    def __init__(self):
        self.logger = logging.getLogger()
        self.LOG_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.file_handel = logging.FileHandler('guidance.log', encoding='utf-8')
        self.file_handel.setFormatter(self.LOG_FORMAT)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handel)
        # self.run_log()

    def get_logger(self):
        return self.logger

    def run_log(self):
        # 打印时间
        self.logger.info('*' * 25)
        self.logger.info("Star:" + datetime.datetime.now().strftime("%Y-%m-%d"))
        self.logger.info('*' * 25)
