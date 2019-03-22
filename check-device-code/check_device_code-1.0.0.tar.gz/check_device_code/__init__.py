# !/usr/bin/python
# coding:utf-8

import re


def __make_imei(imei_str: str):
    # 奇数位之和
    even_Sum = 0
    # 偶数位之和
    odd_Sum = 0
    for i in range(len(imei_str)):
        if (i + 1) % 2 == 0:
            odd_Sum += ((int(imei_str[i]) * 2) // 10) + ((int(imei_str[i]) * 2) % 10)
        else:
            even_Sum += int(imei_str[i])
    check_code = (10 - ((odd_Sum + even_Sum) % 10))
    check_code = 0 if check_code == 10 else check_code
    return ''.join([imei_str, str(check_code)])


def __make_emid(emid_str: str):
    pass


def check_device_code(type: str, code: str):
    if type == 'imei':
        # 判断 imei 为15位数字
        if re.match(r'^\d{15}$', code):
            # 取前14位数字，生成15位的完整imei号码
            new_imei = __make_imei(re.match(r'^(\d{14})\d$', code).group(1))
            # 判断前后两个imei值是否相等
            if code == new_imei:
                # 返回 True，返回原始的imei
                return {'check': True, 'imei': code}
            else:
                # 返回 False，返回正确的imei
                return {'check': False, 'imei': new_imei}
        # 判断 imei 为14位数字
        elif re.match(r'^\d{14}$', code):
            # 返回 False，返回完整的imei
            return {'check': False, 'imei': __make_imei(str(code))}
        else:
            # 返回 False，返回None
            return {'check': False, 'imei': None}
    elif type == 'emid':
        __make_emid(code)
    else:
        raise RuntimeError('getCheckCode type error')
