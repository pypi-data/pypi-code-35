# -*- coding: utf-8 -*-
from .imageopt import handler

import argparse
__VERSION__ = '0.1.0'
def opt():
    parser = argparse.ArgumentParser(description='图片压缩工具')

    parser.add_argument('-d', '--diff',  metavar='',
                        help='压缩的文件是否采用git diff')
    parser.add_argument('-opt', '--Optimizer', default='pngquant',  metavar='(4~30)',
                        help='图片优化器')
    parser.add_argument('-q', '--quality', default='8', type=int, metavar='(0~10)',
                        help='图片质量')
    parser.add_argument('-f', '--force', 
                        help='是否覆盖原图片')


    # # parser.add_argument('-i', '--in', metavar='IN', help='image to convert', required=True)
    # parser.add_argument('-o', '--out', default=None, metavar='OUT',
    #                     help='output file')
    parser.add_argument('-v', '--version', action='version',version=f'%%(prog)s {__VERSION__}')

    args, text = parser.parse_known_args()
    handler(args,text)
    # print(args)
    # print(text)
    # for line in os.popen('git diff --name-only').readlines():
    #     print(line)
    # print('参数个数为:', len(sys.argv), '个参数。')
    # print('参数列表:', str(sys.argv))
    # print('脚本名为：', sys.argv[0])
    # for i in range(1, len(sys.argv)):
    #     print('参数 %s 为：%s' % (i, sys.argv[i]))
