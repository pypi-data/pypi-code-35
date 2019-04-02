#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

def get_os_from_file():
    files=["/etc/redhat-release","/etc/SuSE-release","/etc/release","/etc/issue"]
    for afile in files:
        exist =  os.path.exists(afile)
        if exist:
            #print afile
            f=open(afile,'r')
            while True:
                line=f.readline()
                if not line:
                    f.close()
                    print("The operating system can not resolved")
                    exit(1)
                    break
                if line.find("openSUSE") != -1 or line.find("release")!=-1 or line.find("Mint") != -1:
                    f.close()
                    return line.replace("\n","")
                    break
            f.close()
            print("The operating system can not resolved")
            exit(1)
            break
    print("The operating system can not resolved")
    exit(1)
   
        

if __name__=="__main__":
    print(get_os_from_file())
