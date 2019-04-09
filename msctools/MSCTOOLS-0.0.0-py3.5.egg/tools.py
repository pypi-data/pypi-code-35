#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def sayhi():
    print('hello world')


def readTxt2Lines(txt_file_path):
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

def writeLines2Txt(lines, name):
    f = open(name,'w')
    temp = ''
    for idx, name in enumerate(lines):
        if idx == len(lines)-1 :
            temp += name
        else:
            temp += name + '\n'
    f.write(temp)
    f.close()

def walkDir2List(path):
    root_lists = []
    for fpathe,dirs,fs in os.walk(path):
        # 返回的是一个三元tupple(dirpath, dirnames, filenames),
        for f in fs:
            # print
            root_lists.append(f)
    return root_lists

def walkDir2RealPathList(path):
    root_lists = []
    for fpathe,dirs,fs in os.walk(path):
        # 返回的是一个三元tupple(dirpath, dirnames, filenames),
        for f in fs:
            # print
            root_lists.append(os.path.join(fpathe, f))
    return root_lists

def pathExit(path):
    if isinstance(path, list):
        for ipath in path:
            if not os.path.exists(ipath):
                os.makedirs(ipath)
    else:
        if not os.path.exists(path):
            os.makedirs(path)

class ProgressBar():

    def __init__(self, max_steps):
        self.max_steps = max_steps
        self.current_step = 0
        self.progress_width = 50

    def update(self, step=None):
        self.current_step = step

        num_pass = int(self.current_step * self.progress_width / self.max_steps) + 1
        num_rest = self.progress_width - num_pass
        percent = (self.current_step+1) * 100.0 / self.max_steps
        progress_bar = '[' + '■' * (num_pass-1) + '▶' + '-' * num_rest + ']'
        progress_bar += '%.2f' % percent + '%'
        if self.current_step < self.max_steps - 1:
            progress_bar += '\r'
        else:
            progress_bar += '\n'
        sys.stdout.write(progress_bar)
        sys.stdout.flush()
        if self.current_step >= self.max_steps:
            self.current_step = 0



def main():
    pass




if __name__ == "__main__":
    main()