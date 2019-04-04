#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
 db module, support sqlite3 and mysql
"""

import os,sys
import re

import pymysql


class Database:
    def __init__(self,host,username,password,dbname="",params={}):
        self.CONNECTION=None
        self.CURSOR=None

        params['host']=host
        params['user']=username
        params['passwd']=password
        params['db']=dbname

        #params['conv']=conv
        params['charset']="utf8"
        params['cursorclass']=pymysql.cursors.DictCursor

        self.CONNECTION=pymysql.connect(**params)
        self.CURSOR=self.CONNECTION.cursor()

        self.CURSOR.execute('set names utf8')
        self.CONNECTION.commit()

        #sql="set character_set_database =  utf8"
        #CURSOR.execute(sql)
        #CONNECTION.commit()

        #sql="set character_set_server =  utf8"
        #CURSOR.execute(sql)
        #CONNECTION.commit()



    def disconnect(self):
        self.CURSOR.close()
        self.CONNECTION.close()

        return True

    def fetchAll(self,sql,params=None):
        try:
            if params:
                self.CURSOR.execute(sql,params)
                self.CONNECTION.commit()
            else:
                self.CURSOR.execute(sql)
                self.CONNECTION.commit()

            result=self.CURSOR.fetchall()

        except BaseException as e:
            print(sql)
            print("\t", e)

            return False

        return result

    def fetchOne(self,sql,params=None):
      try:
        if params:
          self.CURSOR.execute(sql,params)
          self.CONNECTION.commit()
        else:
          self.CURSOR.execute(sql)
          self.CONNECTION.commit()

      except BaseException as e:
        print(sql)
        print("\t", e)

        return False


      else:
        result=self.CURSOR.fetchone()
        if not result:
          return False

        if(len(result) != 1):
          raise BaseException("fetchone should only have one field as result")

        if result :
          for k,v in result.items():
            return v

    def fetchRow(self,sql,params=None):
      try:
        if params:
          self.CURSOR.execute(sql,params)
          self.CONNECTION.commit()
        else:
          self.CURSOR.execute(sql)
          self.CONNECTION.commit()
      except BaseException as e:
        print(sql)
        print("\t", e)
        return False

      else:
        result=self.CURSOR.fetchone()
        if result :
          return result
        else:
          return False


    def execute(self,sql,params=None):
      try:
        if params:
          self.CURSOR.execute(sql,params)
          self.CONNECTION.commit()
        else:
          self.CURSOR.execute(sql)
          self.CONNECTION.commit()

        #MySQLdb.paramstyle="qmark"
        #print MySQLdb.paramstyle

      except BaseException as e:
        print(sql)
        print(params)
        print("\tError:\t", e)

        self.CONNECTION.rollback()
        return False

      else:
        self.CONNECTION.commit()

      return True

    def last_insert_id(self):
      return self.CURSOR.lastrowid


    def table(self,table_name,primary="id"):
        return Table(self,table_name,primary)


class Table:
    def __init__(self,db,table_name,primary="id"):
        self.db=db

        self.table_name=table_name
        self.primary=primary

    def getAll(self,where={}):
        where_condition,sql_params=self.build_where(where)

        sql="select * from %s %s" %(self.table_name,where_condition)

        return self.db.fetchAll(sql,sql_params)


    def get(self,primary):
        where={self.primary:primary}
        return self.getRow(where)

    def getRow(self,where={}):
        where_condition,sql_params=self.build_where(where)

        sql="select * from %s %s" %(self.table_name,where_condition)

        return self.db.fetchRow(sql,sql_params)


    def getOne(self,where={},field="id"):
        where_condition,sql_params=self.build_where(where)

        sql="select %s from %s %s" %(field,self.table_name,where_condition)

        return self.db.execute(sql,sql_params)


    def insert(self,data):
        keys='`'+"`,`".join(data.keys())+'`'
        values=list(data.values())

        sql_params=",".join(["%s",]*len(values))

        sql="insert into %s (%s)  values(%s)" %(self.table_name,keys,sql_params)
        self.db.execute(sql,values)

        return self.db.last_insert_id()

    def update(self,where,data):
        if len(data) == 0:
            return ''

        if type(where) in (type('a'),type(1)):
            primary=where
            where={self.primary:primary}

        set_condition=''

        sql_params=[]
        set_conditions=[]
        for k,v in data.items():
          set_conditions.append("`"+k+"`=%s")
          sql_params.append(v)
        set_condition=",".join(set_conditions)

        #
        where_condition,params=self.build_where(where)
        sql_params.extend(params)

        sql="update %s set %s %s" %(self.table_name,set_condition,where_condition)
        #print(sql,sql_params)

        #print sql 
        #print sql_params
        return self.db.execute(sql,sql_params)


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

        where_condition,sql_params=self.build_where(where)


        #
        sql="delete from  %s %s" %(self.table_name,where_condition)

        #print sql 
        #print sql_params
        return self.db.execute(sql,sql_params)


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

        where_condition,sql_params=self.build_where(where)


        #
        sql="select * from  %s %s" %(self.table_name,where_condition)

        try:
            self.CURSOR.execute(sql,sql_params)
            self.CONNECTION.commit()
        except BaseException as e:
          print(sql)
          print(sql_params)
          print("\t", e)

        else:
          result=self.CURSOR.fetchone()
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

    def build_where(self,where={}):
        if len(where) == 0:
            return ("",[])

        if type(where) == type({}):
            sql_params=[]
            where_conditions=[]
            for k,v in where.items():
                where_conditions.append("`"+k+"`=%s")
                sql_params.append(v)

            where_condition=" and ".join(where_conditions)
            where_condition=" where "+where_condition

        if type(where) == type([]):
            sql_params=[]
            where_conditions=[]

            for row in where:
                if len(row) == 2:
                    where_conditions.append("`"+row[0]+"`=%s")
                    sql_params.append(row[1])

                elif len(row) == 3:
                    where_conditions.append("`"+row[0]+"` " +row[1]+"  %s")
                    sql_params.append(row[2])

            where_condition=" and ".join(where_conditions)
            where_condition=" where "+where_condition


        return (where_condition,sql_params)


    def build_set(self,data):
      if len(data) == 0:
        return ''

      set_condition=''

      for k,v in data.items():
        set_condition+=" `%s`='%s' and" %(k,v)

      set_condition=set_condition.rstrip("and")

      return set_condition



###extra
def get_tables(database):
  tables=[]

  rows=fetchAll("show tables in "+database)
  for row in rows:
    name= row.values()[0]
    tables.append(name)

  return tables
