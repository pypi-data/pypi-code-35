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
        coding = 'utf-8_sig'
        # print('处理文件', path)
        end = path+".jieba"
       
        text = ''
        if raw_text = self.open_file(path):
            fileObject = open(end, 'w', encoding='utf-8')
            raw_text = self.clear(raw_text)
            print(raw_text)
            # word = jieba.cut(raw_text, cut_all=True)
            word = jieba.cut_for_search(raw_text, HMM=True)  # 搜索引擎模式

        #     print(word)
            for i in word:
                text = text + i + " "
            #     fileObject.write(final)

            # print(final)
            text = self.clear(text)
            fileObject.write(text)
            fileObject.close()
        return False

    def jieba_path(self, path, type='txt'):
        for file in self.file_List(path, 'txt'):
            # print(file)

            self.jieba_file(file)
    # 合并多个文件

    def file_to_one(self, path, type='jieba', endType='end'):
        final = ''
        fileObject = open(path+'all.'+endType, 'w', encoding='utf-8')
        for file in self.file_List(path, type):
            # print(file)
            fileObj = self.open_file(file)
            # print(fileObj)

            final = final + fileObj + '\n'
            # fileObj.close()
        fileObject.write(final)
        fileObject.close()
    # 兼容编码打开文件

    def open_file(self, file):
        if os.path.isfile(file):
            try:
                fileObj = open(file, encoding='utf-8').read()  # 读入文件
            except:
                fileObj = open(file, encoding='gbk').read()  # 读入文件
            return fileObj
        else:
            return False
    # 清理多余的换行空格等
    def clear(self, string):

        # return string.strip()
        # for line in string.readlines():
        # string = re.sub('[\n]+', '\n', string)
        string = string.replace('\n', '').replace(
            '\n\n', '\n').replace('\r\n', '\n')
        # string = string.replace('\n\n', ' ').replace('\n', '')
        string = re.sub(' +', ' ', string)
        return string

# 执行分词目录
# jieba_path(path)
