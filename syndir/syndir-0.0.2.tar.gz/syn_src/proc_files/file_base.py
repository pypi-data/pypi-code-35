# coding:utf-8
"""
author: sixi
datetime: 2019/4/3
python version: 3.x
summary: 文件扫描，拷贝等操作
install package:
"""
import os
import shutil

from syn_src.base_cls.basic_cls import BaseCls


class FileHandle(BaseCls):
    def __init__(self):
        super().__init__()

    @staticmethod
    def cp_f(src: str, target: str) -> tuple:
        """拷贝文件"""

        def _inner(_src, _target):
            os.makedirs(os.path.dirname(_target), exist_ok=True)
            shutil.copy(_src, _target)

        return super().exec_func(_inner, src, target)

    @staticmethod
    def del_f(path: str) -> tuple:
        """删除文件"""
        return super().exec_func(os.remove, path)

    @staticmethod
    def get_mtime(path: str) -> float:
        """获取文件的修改时间"""
        return os.stat(path).st_mtime

    @staticmethod
    def is_file(path: str) -> bool:
        """判断是否是文件"""
        return os.path.exists(path) and os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        """判断是否是目录"""
        return os.path.exists(path) and os.path.isdir(path)


if __name__ == '__main__':
    fh = FileHandle()
