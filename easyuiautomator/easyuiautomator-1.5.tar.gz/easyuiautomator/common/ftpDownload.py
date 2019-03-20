#coding=utf-8
'''
Created on 2017年8月3日

@author: Administrator
'''
import ftplib, os, shutil

from easyuiautomator.common.log import Logger


HOST = "172.16.15.130"
class FtpDownLoad(object):
    
    def __init__(self,host=HOST):
        self.host = host
        self.ftp = ftplib.FTP()
        self.ftp.set_pasv(0) #0 主动模式 1 #被动模式
#         self.ftp.set_debuglevel(2)
        self.bufsize = 1024  #设置缓冲块大小 
        self.logger = Logger.getLogger()

    def _login(self):
        '''登录服务器'''
        try:
            self.ftp.connect(self.host)
            self.ftp.login()
            return True
        except:
            return False
    
    def _rmDir(self,dirname):
        '''删除整个目录结构'''
        try:
            shutil.rmtree(dirname)
        except:
            pass
        
    def downLoadDir(self, remotedir, localdir='.'):
        '''下载远程目录'''
        if self._login():
            path = os.path.join(os.path.abspath(localdir), os.path.basename(remotedir))
            if os.path.exists(path):
                self._rmDir(path)
            os.chdir(os.path.abspath(localdir))
            self._downLoadDir(remotedir)
            os.chdir(os.path.abspath(localdir))
            self.close()
            return True
        else:
            return False
        
    def _downLoadDir(self, remotedir):
        '''下载远程目录'''
        rdir = os.path.basename(remotedir)
        os.makedirs(rdir)
        os.chdir(rdir) 
        self.ftp.cwd(remotedir)
        filelines = []  
        self.ftp.dir(filelines.append)  
        filelines_bk = self.ftp.nlst()
        i = 0
        for file in filelines:
            if 'd' in file.split()[0]: 
                self._downLoadDir(filelines_bk[i].decode("utf-8"))
                self.ftp.cwd('..')  
                os.chdir('..')  
            else:
                newFileName = filelines_bk[i].decode("utf-8")
                fd = open(newFileName, 'wb')  
                self.ftp.retrbinary('RETR %s'%filelines_bk[i], fd.write)  
                fd.close() 
                self.logger.debug(newFileName)
            i += 1
        
     
    def downLoadFile(self, remote_file, local_file='.'):
        '''下载单个文件'''
        if self._login():
            if os.path.isdir(local_file):
                local_file = os.path.join(local_file, os.path.basename(remote_file)) 
            file_handler = open(local_file, 'wb')
            try:
                self.ftp.retrbinary('RETR %s'%(remote_file), file_handler.write)  
            except:
                pass
            finally:
                if file_handler:
                    file_handler.close()
                self.close()
                self.logger.debug(remote_file)
            if os.path.getsize(local_file) > 0:
                return True
            else:
                os.remove(local_file)
                return False
        return False   
        
    def close(self):
        '''关闭ftp'''
        if self.ftp:
            self.ftp.quit()
            self.ftp = None
    
    def test(self):
        if self._login():
            self.ftp.cwd("test/我是中国人")
        
if __name__ == '__main__':
    a = FtpDownLoad()
    print a.downLoadDir("ageingtest", "d://tmp//", )
    a.close()
    