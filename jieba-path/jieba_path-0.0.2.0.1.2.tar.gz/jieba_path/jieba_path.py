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
        
        print('working:',path)
        text = ''
        try :
            raw_text = self.open_file(path)
        except:
            return False
        
        fileObject = open(end, 'w', encoding='utf-8')
        raw_text = self.clear(raw_text)
        # print(raw_text)
                # word = jieba.cut(raw_text, cut_all=True)
        # word = jieba.cut_for_search(raw_text, HMM=True)  # 搜索引擎模式
        word = jieba.cut(raw_text)  # 使用默认模式
            #     print(word)
        for i in word:
            text = text + i + " "
                #     fileObject.write(final)

                # print(final)
        text = self.clear(text)
        fileObject.write(text)
        fileObject.close()
                # raw_text.close()

    def jieba_file_noclear(self, path):
        coding = 'utf-8_sig'
        # print('处理文件', path)
        end = path+".jieba"
       
        text = ''
        try :
            raw_text = self.open_file(path)
        except:
            return False
        
        fileObject = open(end, 'w', encoding='utf-8')
        # raw_text = self.clear(raw_text)
        # print(raw_text)
                # word = jieba.cut(raw_text, cut_all=True)
        # word = jieba.cut_for_search(raw_text, HMM=True)  # 搜索引擎模式
        word = jieba.cut(raw_text)  # 使用默认模式

            #     print(word)
        for i in word:
            text = text + i + " "
                #     fileObject.write(final)

                # print(final)
        # text = self.clear(text)
        fileObject.write(text)
        fileObject.close()
                # raw_text.close()
        

    def jieba_path(self, path, type='txt'):
        for file in self.file_List(path, 'txt'):
            # print(file)

            self.jieba_file(file)
    # 合并多个文件
    def jieba_path_noclear(self, path, type='txt'):
        for file in self.file_List(path, 'txt'):
            # print(file)

            self.jieba_file_noclear(file)
    def file_to_one(self, path, type='jieba', endType='end'):
        final = ''
        fileObject = open(path+'all.'+endType, 'w', encoding='utf-8')
        for file in self.file_List(path, type):
            # print(file)
            try :
                fileObj = self.open_file(file)
            except:
                # return False
                continue
            
            # print(fileObj)

            final = final + fileObj + '\n'
            # fileObj.close()
        fileObject.write(final)
        fileObject.close()

    def cut_p(self, file,endType='end'):
        final = ''
        fileObject = open(path+'cut_p.'+endType, 'w', encoding='utf-8')

        try :
            fileObj = self.open_file(file)
        except:
            return False
            # continue
        final = re.split('(。|！|\!|\.|？|\?)',fileObj)
        # final = fileObj.replace('。', '\n').replace(
        #     '？', '\n').replace('！', '\n').replace('！', '\n')  
            # print(fileObj)

            # final = final + fileObj + '\n'
            # fileObj.close()
        fileObject.write(final)
        fileObject.close()
        return final
    # 兼容编码打开文件

    def open_file(self, file):
        print('open_file',file)
        if os.path.isfile(file):
            print('open_file 存在',file)
            try:
                fileObj = open(file, encoding='utf-8').read()  # 读入文件
                print('utf8',file)
            except:
                fileObj = open(file, encoding='gbk').read()  # 读入文件
                print('尝试gbk打开',file)
            print('open_file 成功',file)
            return fileObj
        else:
            print('open_file 失败',file)
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
