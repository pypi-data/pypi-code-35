# -*- coding: utf-8 -*-
from utools.bin import pngquant
from .optconfig  import configs as def_config
import os
import sys
import argparse


__config__=os.path.join(os.path.dirname(__file__),"optconfig.py")

def handler(args, text):
    opt = ImageOpt()
    opt.optimize()


class IGit(object):

    @staticmethod
    def get_git_root_dir():
        lines = os.popen('git rev-parse --show-toplevel').readlines()
        if(len(lines) > 0):
            return lines[0].strip()

    @staticmethod
    def get_cache_diff_files():
        difffiles = []
        lines = os.popen('git diff --cached  --name-only').readlines()
        for line in lines:
            difffiles.append(line.strip())
        return difffiles


class ImageOpt(object):
    workdirname = '.utools'
    workdirpath = ''
    git_root_path =''

    def __init__(self, *args, **kwargs):
        self.git_root_path = IGit.get_git_root_dir()
        self.workdirpath = self.git_root_path+"/"+self.workdirname

    def createworkspace(self, configs):
        workdirpath = os.path.exists(self.workdirpath)
        if not workdirpath:
            a = input("无工程目录，是否创建(.utools)(Y/n)？")
            if str(a).strip() == 'y' or str(a).strip() == 'Y' or str(a).strip() == '':
                self._create_workspace()
                return self._create_config(configs)
            elif a == 'n' or a == 'N':
                print("取消创建工程目录")
            else:
                print("工程目录创建失败")
        else:
            configs_path = self.workdirpath+"/config.py"
            if not os.path.exists(configs_path):
                b= input('当前无配置文件，是否创建？(Y/n)')
                if str(b).strip()=='' or str(b).strip() == 'Y' or str(b).strip()=='y':
                    return self._create_config(configs)
            else:
                return True
        return False

    def _create_workspace(self):
        # 创建工作目录
        os.makedirs(self.workdirpath)
        print('工程目录创建成功')

    def _create_config(self, configs):
        import shutil
        shutil.copyfile(__config__,
                        self.workdirpath+"/config.py")
        print('配置文件创建成功')
        a = input("是否以一下配置来进行:\n"+str(configs)+"\n(y/N)？")
        if str(a).strip() == 'y' or str(a).strip() == 'Y':
            return True
        return False

    def readconfig(self):
        # 读取
        configs: dict = def_config
        try:
            import imp
            config = imp.load_source(
                'config', self.workdirpath+"/config.py")
            from config import configs as newconfigs
            configs.update(newconfigs)
        except Exception as e:
            print(e)
        return configs

    def optimize(self):
        configs = self.readconfig()
        next_step=self.createworkspace(configs)
        print(next_step)
        if not next_step:
            return
        
        cache_diff = IGit.get_cache_diff_files()
        print(configs['ext'])
        if configs['ext']:
            filter_diff = self._filter_by_ext(
                cache_diff, configs['ext'])
        if not filter_diff:
            return
        filter_diff=list(map(lambda x:os.path.join(self.git_root_path,x),filter_diff))
        if configs['safe']:
            print(filter_diff)
            self._safe_copy(configs,filter_diff)
            self._pngquant(filter_diff,True)
        else:
            if configs['force']:
                self._pngquant(filter_diff,True)
            else:
                self._pngquant(filter_diff,False)
        
    def _safe_copy(self,configs,files):
        # 创建临时文件夹
        tmp_dir=configs['safe_dir']
        if not tmp_dir:
            tmp_dir='tmp'
        tmp_dir=os.path.join(self.workdirpath,tmp_dir)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        
        # 创建记录文件
        import time
        now = int(time.time())
        import shutil
        print(f"ff")
        with open(os.path.join(self.workdirpath,tmp_dir,str(now)+'.recode'), 'a') as rcd:
            for f in files:
                print(f)
                rcd.writelines(str(now)+"\t"+f+"\n")
                shutil.copyfile(f, os.path.join(tmp_dir,str(now)+'.tmp'))
                now=now+1

    def _pngquant(self,files,force):
        if force:
            for f in files:
                f=f.replace(' ','\ ')
                cmd = " ".join([pngquant,f,"--output",f,"--force"])
                print(cmd)
                lines = os.popen(cmd).readlines()
                for line in lines:
                    print(line)
        else:       
            for f in files:
                f=f.replace(' ','\ ')
                cmd = " ".join([pngquant,f,"--output",f])
                lines = os.popen(cmd).readlines()
                for line in lines:
                    print(line)
                    
    def _filter_by_ext(self, files: list = [], ext: list = ['.png']):
        return list(filter(lambda f: os.path.splitext(f)[-1] in ext, files))


if __name__ == "__main__":
    opt = ImageOpt()
    opt.optimize()


    print(os.path.dirname(__file__))

    # git_root_path = IGit.get_git_root_dir()
    # # # print(os.path.exists(git_root_path))
    # IFileManager.workdirpath = git_root_path+"/"+IFileManager.workdirname
    # # import shutil
    # # shutil.copyfile(def_config.__file__,
    # #                 IFileManager.workdirpath+"/config.py")

    # import imp
    # # try:
    # #     config=imp.load_source('config',IFileManager.workdirpath)
    # #     import config.configs
    # #     print(config.configs.ext)
    # # except:
    # #     pass

    # configs:dict=def_config.configs
    # print(configs['record_dir'])
    # # try:
    # config=imp.load_source('config',IFileManager.workdirpath+"/config.py")
    # from config import configs as newconfigs
    # configs.update(newconfigs)
    # # except :
    # #     pass
    # # print(type(configs['record_dir']))
    # print(configs['record_dir'])
    # cache_diff=IGit.get_cache_diff_files()
    # if configs['ext']:
    #     filter_diff=IFileManager.filter_by_ext(cache_diff,configs['ext'])
    #     print(filter_diff)