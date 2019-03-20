import datetime

import requests

import ybc_config

import sys

from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__HISTORY_URL = __PREFIX + ybc_config.uri + '/history'


def history_info(month=datetime.datetime.today().month, day=datetime.datetime.today().day, number=3, type='string'):
    """
    功能：获取历史上的今天。

    参数：month，day：日期，默认今天
         number：事件条数，超出则返回当天所有事件
         type：返回值类型，输入list返回列表，其他则返回string

    返回：历史上的今天事件
    """
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    error_flag = 1
    # 参数类型正确性判断
    error_msg = ""
    if not (isinstance(month, int) or str(month).isdigit()):
        error_flag = -1
        error_msg = "'month'"
    if not (isinstance(day, int) or str(day).isdigit()):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'day'"
    if not (isinstance(number, int) or str(number).isdigit()):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'number'"
    if not isinstance(type, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'type'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    month = int(month)
    day = int(day)
    number = int(number)

    # 参数数值正确性判断
    if month < 1 or month > 12:
        error_flag = -1
        error_msg += "'month'"
    if error_flag == 1 and (day < 1 or day > days[month - 1]):
        error_flag = -1
        error_msg += "'day'"
    if number <= 0:
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'number'"
    if error_flag == -1:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    try:
        params = {
            "month": month,
            "day": day,
            "number": number
        }

        url = __HISTORY_URL
        for i in range(3):
            r = requests.get(url, params)
            if r.status_code == 200:
                res = r.json()
                if len(res) == 0:
                    print("今天没有著名的事件哦～")
                    return -1
                if number > len(res):
                    print("history_info方法使用提示: 超出该天记录事件数，已展示所有事件")

                if type == 'list':
                    return res
                else:
                    return "\n".join(res)

        raise ConnectionError("history_info方法调用失败: 请稍后再试", r.content)
    except Exception as e:
        raise InternalError(e, 'ybc_history')


def main():
    result = history_info(1, 1, 3, "list")
    print(result)


if __name__ == '__main__':
    main()
