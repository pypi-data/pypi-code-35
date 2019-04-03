# coding:utf-8
"""
author: sixi
datetime: 2019/4/3
python version: 3.x
summary: 运行主函数
install package:
"""
from syn_src.proc_files.dir_base import DirHandle


def execute():
    for f in DirHandle.get_dir_tree('.'):
        print(f)
    print('excute cmd demo')


if __name__ == '__main__':
    execute()