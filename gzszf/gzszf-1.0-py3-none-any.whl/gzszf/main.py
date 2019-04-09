# -*- coding: utf-8 -*- 
# @Time : 2019/4/8 13:32 
# @Author : Allen 
# @Site :  定时爬取接口
import schedule
from gzszf.gzszf_interface_guidance import run_guidance


def main():
    run_guidance()


# 定时 每天凌晨1点
schedule.every().day.at("02:00").do(main)

while True:
    schedule.run_pending()
