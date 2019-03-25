#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/3/23 0023
# @Email : jtyoui@qq.com

"""处理二维矩阵"""


class Matrix:

    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("传入list类型")
        self.__data = data

    @property
    def i(self):
        """逆矩阵"""
        return 1

    @property
    def t(self):
        """转置矩阵"""
        return 1

    @property
    def det(self):
        """秩"""
        for i, data in enumerate(self.__data, 1):
            for j, item in enumerate(data, 1):
                if i != j:
                    print(item)
        return 1


if __name__ == '__main__':
    d = [
        [1, 0, 5],
        [2, 1, 6],
        [3, 4, 0]
    ]
    m = Matrix(d)
    print(m.det)
