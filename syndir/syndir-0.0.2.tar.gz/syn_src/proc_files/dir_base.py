# coding:utf-8
"""
author: sixi
datetime: 
python version: 3.x
summary: 目录操作
install package:
"""
import os

from syn_src.base_cls.basic_cls import BaseCls


class DirHandle(BaseCls):
    def __init__(self):
        super().__init__()

    @staticmethod
    def del_dir(path: str) -> tuple:
        """删除目录"""
        return super().exec_func(os.rmdir, path)

    @staticmethod
    def get_dir_tree(path: str) -> str:
        """获取指定目录下的所有文件绝对路径"""
        if path == '.':
            path = os.getcwd()
        if not os.path.isdir(path):
            raise FileNotFoundError("指定目录不存在")
        for t, ps, fs in os.walk(path):
            for f in fs:
                yield os.path.join(t, f)


if __name__ == '__main__':
    DirHandle().get_dir_tree(r'D:\windows_installed\Anaconda\Lib\site-packages')
