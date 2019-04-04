#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
 command module
"""

import re

class CommandLine:
  def __init__(self,string=""):
    self.name=''
    self.params=[]
    self.params_rules={}
    self.options=[]
    self.options_rules={}

    if string:
      self.parseSetting(string)


  def parseSetting(self,string):
    #cl=CommandLine("login :username=frd :password")
    """
    1. 解析 -v --long  选项（optional)
    2. 解析 :userna=xxxx
    3. 剩下的是 name
    """

    #去除首尾空格
    string=string.strip()

    #合并多个空格为单个
    string=re.sub(" +"," ",string)


    cols=string.split(" ")

    cmds=[] #name的每个字段
    params=[]
    params_rules={}


    for col in cols:
      if col[0] == ":":
        col=col[1:]

        if len(col.split("=")) == 1:
          params.append(col)
          params_rules[col]={
            "required":True,
            'default':None,
            'type':None,
          }

        elif len(col.split("=")) == 2:
          items=col.split("=")

          params.append(items[0])
          params_rules[items[0]]={
            "required":True,
            "default":items[1],
            'type':None,
          }

        else:
          raise BaseException("invalid command line")

      else:
        cmds.append(col)


    self.name=".".join(cmds)
    self.params=params
    self.params_rules=params_rules

  def getShort(self):
    print(self.name,':'+" :".join(self.params))

  def getDetail(self):
    print('name',self.name)
    print('params',self.params)
    print('params rules',self.params_rules)
    print('options',self.options)
    print('options rules',self.options_rules)

  def __str__(self):
    if self.params:
        return self.name.replace("."," ")+" "+':'+" :".join(self.params)
    else:
        return self.name.replace("."," ")

class Command:
  def __init__(self):
    self.lines=[]

    self.current={
        'name':None,
        'params':{},
        'options':'', #结果是字符串， 通过 'a' in options来判断选项是否开启
    }

  def addLine(self,line):
    self.lines.append(line)

  def dumpLines(self,indent=""):
    i=0
    for line in self.lines:
      i+=1
      print(indent,i,line)

  def usage(self):
    #print("Command")
    #print("")
    print("Usage:")

    self.dumpLines("\t")

  """
  解析方式:
  1. 逐个command line 进行判断，若 name 符合则认为匹配成功
  2. 对于匹配成功的，进行参数获取和填充
  3. 最后检查参数规则，是否都有值
  4. 仅仅判断第一个匹配的command line,所以要注意command line的次序，必须是复杂的在前
  """
  def parse(self,string):
    self.current={'name':False,'params':{}}

    #去除首尾空格
    string=string.strip()

    if not string :
        return False

    #合并多个空格为单个
    string=re.sub(" +"," ",string)
    cols=string.split(" ")

    for line in self.lines:
      if len(line.name.split(".")) > len(cols): continue

      #result
      name=line.name
      params={}
      options=""

      match=True
      i=0
      for name in line.name.split("."):
        if name != cols[i]:
          match=False
          break

        i+=1

      if not match:continue

      cols=cols[len(line.name.split(".")):]

      ## 首先解析赋值参数
      remain_cols=[]

      ## 提取选项 
      i=0
      for col in cols:
        r=re.match("(-\w+)",col)
        if r:
          options+=r.groups()[0][1:]
        else:
          remain_cols.append(col)

        i+=1


      cols=remain_cols.copy()
      i=0
      for col in cols:
        r=re.match("(\w+)=(\w+)",col)
        if r:
          params[r.groups()[0]]=r.groups()[1]
        else:
          remain_cols.append(col)

        i+=1

      ## 其次按照参数次序获取
      i=0
      for name in line.params:
        if len(remain_cols) > i :
          params[name]=remain_cols[i]

        i+=1


      #check params rules
      for name,rule in line.params_rules.items():
        if rule['default'] and (name not in params ):
          params[name]= rule['default']

      for name,rule in line.params_rules.items():
        if rule['required']:
          if name not in params or params[name] == None:
            raise BaseException("param ["+name+"] is required")


      result=[line.name,params]

      self.current['name']=line.name
      self.current['params']=params
      self.current['options']=options


      return result


    return False


class Handler:
    def do(self,cmd):
        name=cmd['name']
        params=cmd['params']

        name=self.convert_name(name)

        if hasattr(self,name):
            func=getattr(self,name)
            func(params)
        else:
            raise BaseException(name+" not exists")

    def convert_name(self,name):
        return name.replace(".","_")


