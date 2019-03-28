# -*- coding: utf-8 -*-
# 对文件进行预处理
import jieba
import re
import os
# 遍历目录文件夹

# path = "/content/lstm-text-generation/input/"  # 文件夹目录


class Jpath:
    def __init__(self):
        pass

    def file_List(self, path, type='txt'):
        files = []
        for file in os.listdir(path):

            if file.endswith("." + type):
                print(path+file)
                files.append(path+file)
        return files

    # file_List(path)

    # 读取文件并且进行结巴分词处理

    def jieba_file(self, path):
        fileObject = open(path+".jieba", 'w')
        text = ''
        raw_text = open(path, errors='ignore',
                        encoding='utf-8').read()+'\n\n'  # 读入文件
    #   for line in raw_text:
    #     print (line)
        word = jieba.cut(raw_text, cut_all=True)
    #     print(word)
        for i in word:
            text = text + i + " "
        #     fileObject.write(final)

        # print(final)
        fileObject.write(text)

    def jieba_path(self, path, type='txt'):
        for file in self.file_List(path, 'txt'):
            self.jieba_file(file)


# 执行分词目录
# jieba_path(path)
