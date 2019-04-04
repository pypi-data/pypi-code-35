#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
 db module, support sqlite3 and mysql
"""

import os,sys
import re

import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors

CONNECTION=None
CURSOR=None


def check_connnect():
  if not CURSOR  or not CONNECTION:
    raise BaseException("db not connected")


def connect(username,password,dbname,params={}):
  global CONNECTION,CURSOR

  try:
    conv=MySQLdb.converters.conversions.copy()

    #数字定义在 MysqlDb.constants/FILE_TYPE.py
    conv[246]=float    # convert decimals to floats
    conv[10]=str       # convert dates to strings
    conv[12]=str       # convert datetime to strings


    #CONNECTION=MySQLdb.connect(host=host,user=username,passwd=str(password),db=dbname,port=port,charset="utf8",cursorclass=MySQLdb.cursors.DictCursor,conv=conv)
    #CONNECTION=MySQLdb.connect(user=username,passwd=str(password),db=dbname,charset="utf8",cursorclass=MySQLdb.cursors.DictCursor,conv=conv)

    params['user']=username
    params['passwd']=unicode(password)
    params['db']=dbname

    params['conv']=conv
    params['charset']="utf8"
    params['cursorclass']=MySQLdb.cursors.DictCursor

    CONNECTION=MySQLdb.connect(**params)


    CURSOR=CONNECTION.cursor()

    CURSOR.execute('set names utf8')
    CONNECTION.commit()

    sql="set character_set_database =  utf8"
    CURSOR.execute(sql)
    CONNECTION.commit()

    sql="set character_set_server =  utf8"
    CURSOR.execute(sql)
    CONNECTION.commit()



  except MySQLdb.Error as e:
    print("Mysql Error %d: %s" %(e.args[0], e.args[1]))
    return False

  else:
    return True



def disconnect():
  CURSOR.close()
  CONNECTION.close()

  return True



def fetchAll(sql,params=None):
  check_connnect()

  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()
  except BaseException as e:
    print(sql)
    print("\t", e)

  else:
    result=CURSOR.fetchall()
    return result

def fetchOne(sql,params=None):
  check_connnect()

  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()

  except BaseException as e:
    print(sql)
    print("\t", e)


  else:
    result=CURSOR.fetchone()
    if result :
      for k,v in result.items():
        return v
    else:
      return False

def fetchRow(sql,params=None):
  check_connnect()
  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()
  except BaseException as e:
    print(sql)
    print("\t", e)

  else:
    result=CURSOR.fetchone()
    if result :
      return result
    else:
      return False


def execute(sql,params=None):
  try:
    if params:
      CURSOR.execute(sql,params)
      CONNECTION.commit()
    else:
      CURSOR.execute(sql)
      CONNECTION.commit()

    #MySQLdb.paramstyle="qmark"
    #print MySQLdb.paramstyle

  except BaseException as e:
    print(sql)
    print(params)
    print("\tError:\t", e)
    return False

  else:
    CONNECTION.commit()

  return True

def last_insert_id():
  return CURSOR.lastrowid


##
def build_where(where={}):
  if len(where) == 0:
    return ("",[])

  sql_params=[]
  where_conditions=[]
  for k,v in where.items():
    where_conditions.append("`"+k+"`=%s")
    sql_params.append(v)
  where_condition=" and ".join(where_conditions)

  where_condition=" where "+where_condition


  return (where_condition,sql_params)

def build_set(data):
  if len(data) == 0:
    return ''

  set_condition=''

  for k,v in data.items():
    set_condition+=" `%s`='%s' and" %(k,v)

  set_condition=set_condition.rstrip("and")

  return set_condition

class Table:
  def __init__(self,table_name,primary="id"):
    self.table_name=table_name
    self.primary=primary

  def getAll(self,where={}):
    where_condition,sql_params=build_where(where)

    sql="select * from %s %s" %(self.table_name,where_condition)

    try:
      CURSOR.execute(sql,sql_params)
      CONNECTION.commit()
    except BaseException as e:
      print(sql)
      print("\t", e)

    else:
      result=CURSOR.fetchall()
      return result

  def get(self,primary):
    where={self.primary:primary}
    return self.getRow(where)

  def getRow(self,where={}):
    where_condition,sql_params=build_where(where)

    sql="select * from %s %s" %(self.table_name,where_condition)


    try:
      CURSOR.execute(sql,sql_params)
      CONNECTION.commit()
    except BaseException as e:
      print(sql)
      print("\t", e)

    else:
      result=CURSOR.fetchone()
      if result :
        return result
      else:
        return False

  #def getOne(self,where={},field):
  def getOne(self,where={},field="id"):

    where_condition,sql_params=build_where(where)

    sql="select %s from %s %s" %(field,self.table_name,where_condition)

    try:
      CURSOR.execute(sql,sql_params)
      CONNECTION.commit()
    except BaseException as e:
      print(sql)
      print("\t", e)

    else:
      result=CURSOR.fetchone()
      if result :
        for k,v in result.items():
          return v
      else:
        return False


  def insert(self,data):
    keys='`'+"`,`".join(data.keys())+'`'
    values=data.values()

    sql_params=",".join(["%s",]*len(values))

    sql="insert into %s (%s)  values(%s)" %(self.table_name,keys,sql_params)

    execute(sql,values)

    return CURSOR.lastrowid

  def update(self,where,data):
    if not ( type(where) == type({}) ):
      primary=where
      where={self.primary:primary}

    if len(data) == 0:
      return ''


    #sql="update %s set 
    set_condition=''

    sql_params=[]
    set_conditions=[]
    for k,v in data.items():
      set_conditions.append("`"+k+"`=%s")
      sql_params.append(v)
    set_condition=",".join(set_conditions)

    #
    where_conditions=[]
    for k,v in where.items():
      where_conditions.append("`"+k+"`=%s")
      sql_params.append(v)
    where_condition=" and ".join(where_conditions)

    
    #
    sql="update %s set %s where %s" %(self.table_name,set_condition,where_condition)

    #print sql 
    #print sql_params
    return execute(sql,sql_params)

  """
  two usage 

  delete(primary)
  delete(where)
  """
  def delete(self,where):
    if not ( type(where) == type({}) ):
      primary=where
      where={self.primary:primary}

    if len(where) == 0:
      return ''

    where_condition,sql_params=build_where(where)

    
    #
    sql="delete from  %s %s" %(self.table_name,where_condition)

    #print sql 
    #print sql_params
    return execute(sql,sql_params)


  def existsWhere(self,where):
    return self.exists(where)

  """
  two usage 

  exists(primary)
  exists(where)
  """
  def exists(self,where):
    if not ( type(where) == type({}) ):
      primary=where
      where={self.primary:primary}


    if len(where) == 0:
      return ''

    where_condition,sql_params=build_where(where)

    
    #
    sql="select * from  %s %s" %(self.table_name,where_condition)

    try:
        CURSOR.execute(sql,sql_params)
        CONNECTION.commit()
    except BaseException as e:
      print(sql)
      print(sql_params)
      print("\t", e)

    else:
      result=CURSOR.fetchone()
      if result :
        return True
      else:
        return False

  #复合函数
  #insert where
  #if where exists: update
  #else insert
  def insertWhere(self,where,data):
    if self.exists(where):
      return self.update(where,data)
    else:
      return self.insert(data)


  #update where 
  #if where exists, update
  #else do nothing
  def updateWhere(self,where,data):
    if self.exists(where):
      self.update(where,data)

  #delete where
  #if where exists : delete
  def deleteWhere(self,where):
    if self.exists(where):
      self.delete(where)
      return True
    else:
      return False



###extra
def get_tables(database):
  tables=[]

  rows=fetchAll("show tables in "+database)
  for row in rows:
    name= row.values()[0]
    tables.append(name)

  return tables
