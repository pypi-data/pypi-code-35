name = "vtemplate"
import sys
import os, errno
import datetime

class create:
    
    def licence(self,t):
        loc = t + '/LICENCE'
        text = '''All the rights for this software vests with VIRTUSA 
    
    Usage of this software is strictly prohibited without a agreement from Virtusa
    
    if you are an employee of Virtusa, you are vested with rights to modify and use this software inside virtusa network but strictly prohibited to use this outside the virtusa network
    
    By using this software you agreeing to above rules'''
        file = open(loc,'w')
        file.write(text)
        file.close()
        print('created LICENCE')
        return
    
    def readme(self,t):
        today = datetime.date.today()
        loc = t + '/README.md'
        text = '''#######
    --author details--
    date of creation = {}
    author = {}
    email = {}
    phone = {}
    city = {}
    country = {}
    ###please add you details if you are modifying as follows
    ###--modifier1--
    ###date=
    ###name=
    ###email=
    ###phone=
    ###country=
    #######
    Small description of project and how to run goes here'''
        name = input('enter your name :')
        email = input('enter your Email id :')
        phone = input('enter your phone no.:')
        city = input('enter your city :')
        country = input('enter your country :')
        file = open(loc,'w')
        file.write(text.format(today,name,email,phone,city,country))
        file.close()
        print('created README.md')
        return
    
    def requirements(self,t):
        loc = t + '/requirements.txt'
        text = '''##please add the libraries along with version with '=='
    ##exmaple (add withut hashtags and no punctuations)
    #pandas==0.24.1
    #flask==1.0.2
    ##please use double equals as this files will be directly used in a cmd
    ##to install all requiements use 'pip install -r /path/to/requirements.txt'''
        file = open(loc,'w')
        file.write(text)
        file.close()
        print('created requirements.txt')
        return
    
    def folder(self,t,name):
        try:
            os.makedirs(t+'/'+name)
            print('created {} directory'.format(name))
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('folder {} already exists'.format(name))
                overwrite = input("do you want to overwrite?[y&n] - ")
            if overwrite == 'n':
                sys.exit()
        return 
    
    def flsbis(self,t,name):
        try:
            os.makedirs(t+'/Demo/'+name)
            print('created {} directory'.format(name))
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('folder {} already exists'.format(name))
                overwrite = input("do you want to overwrite?[y&n] - ")
            if overwrite == 'n':
                sys.exit()
        return 
   
    def __init__(self,name): 
        self.name = name
        try:
            os.makedirs(self.name)
            print('created master directory')
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('folder already exists')
                overwrite = input("do you want to overwrite?[y&n] - ")
            if overwrite == 'n':
                sys.exit()   
        print('choose a choice from 1-4\n\n\n 1.Raw code\n 2.Flask bisected(api format)\n 3.Flask integrated\n 4.python library\n\nEnter the number of the choice, example: enter 1 for raw code structure')
        self.selection = input("Enter Number of choice selected  - ")
        if self.selection not in ['1','2','3','4']:
            print('choose a valid response between 1-4')
            sys.exit()
        #print('you entered '+selection)
        if self.selection == '1':
            self.folder(self.name,'code')
            self.folder(self.name,'PPT')
            self.folder(self.name,'Demo')
            self.readme(self.name)
            self.requirements(self.name)
            self.licence(self.name)
            print('created {} with Raw code structure'.format(self.name))
            
        elif self.selection == '2':
            self.folder(self.name,'code')
            self.folder(self.name,'PPT')
            self.folder(self.name,'Demo')
            self.flsbis(self.name,'frontend')
            self.flsbis(self.name,'backend')
            self.readme(self.name)
            self.requirements(self.name)
            self.licence(self.name)
            print('created {} with Flask bisected(api format) structure'.format(self.name))
            
        elif self.selection == '3':
            self.folder(self.name,'code')
            self.folder(self.name,'PPT')
            self.folder(self.name,'Demo')
            self.readme(self.name)
            self.requirements(self.name)
            self.licence(self.name)
            print('created {} with Flask integrated structure'.format(self.name))
            
        elif self.selection == '4':
            self.folder(self.name,'code')
            self.folder(self.name,'PPT')
            self.folder(self.name,'Library') 
            self.readme(self.name)
            self.licence(self.name)
            print('created {} with library structure'.format(self.name))
        