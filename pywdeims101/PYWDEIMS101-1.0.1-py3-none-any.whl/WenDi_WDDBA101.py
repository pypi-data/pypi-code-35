import pymssql
import pymysql
import pyodbc
import cx_Oracle

class DBA_SQLServer:
    def __init__(self, DATA_SOURCE, INITIAL_CATALOG, USER_ID, PASSWORD):
        self.DATA_SOURCE = DATA_SOURCE
        self.INITIAL_CATALOG = INITIAL_CATALOG
        self.USER_ID = USER_ID
        self.PASSWORD = PASSWORD
    
    def __GetConnectCursor(self):
        if not self.INITIAL_CATALOG:
            raise NameError("对不起，未设置数据库名称！")
        
        self.conn = pymssql.connect(host = self.DATA_SOURCE, user = self.USER_ID, password = self.PASSWORD, database = self.INITIAL_CATALOG, charset = "UTF8")
        cursor = self.conn.cursor()

        if not cursor:
            raise NameError("对不起，数据库连接失败!")
        else:
            return cursor
    
    def ExecQuery(self, sqlText):
        cursor = self.__GetConnectCursor()
        cursor.execute(sqlText)
        resultList = cursor.fetchall()

        self.conn.close()

        return resultList
    
    def ExecNonQuery(self, sqlText):
        cur = self.__GetConnectCursor()
        cur.execute(sqlText)
        self.conn.commit()
        self.conn.close()

class DBA_MySQL:
    def __init__(self, DATA_SOURCE, INITIAL_CATALOG, USER_ID, PASSWORD):
        self.DATA_SOURCE = DATA_SOURCE
        self.INITIAL_CATALOG = INITIAL_CATALOG
        self.USER_ID = USER_ID
        self.PASSWORD = PASSWORD
    
    def __GetConnectCursor(self):
        if not self.INITIAL_CATALOG:
            raise NameError("对不起，未设置数据库名称！")
        
        self.conn = pymysql.connect(host = self.DATA_SOURCE, user = self.USER_ID, password = self.PASSWORD, database = self.INITIAL_CATALOG, charset = "UTF8")
        cursor = self.conn.cursor()

        if not cursor:
            raise NameError("对不起，数据库连接失败!")
        else:
            return cursor
    
    def ExecQuery(self, sqlText):
        cursor = self.__GetConnectCursor()
        cursor.execute(sqlText)
        resultList = cursor.fetchall()

        self.conn.close()

        return resultList
    
    def ExecNonQuery(self, sqlText):
        cur = self.__GetConnectCursor()
        cur.execute(sqlText)
        self.conn.commit()
        self.conn.close()

class DBA_AzureSQL:
    def __init__(self, DATA_SOURCE, INITIAL_CATALOG, USER_ID, PASSWORD):
        self.DATA_SOURCE = DATA_SOURCE
        self.INITIAL_CATALOG = INITIAL_CATALOG
        self.USER_ID = USER_ID
        self.PASSWORD = PASSWORD
    
    def __GetConnectCursor(self):
        if not self.INITIAL_CATALOG:
            raise NameError("对不起，未设置数据库名称！")
        
        server = self.DATA_SOURCE
        database = self.INITIAL_CATALOG
        username = self.USER_ID
        password = self.PASSWORD
        driver= '{ODBC Driver 17 for SQL Server}'
        self.conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = self.conn.cursor()

        if not cursor:
            raise NameError("对不起，数据库连接失败!")
        else:
            return cursor
    
    def ExecQuery(self, sqlText):
        cursor = self.__GetConnectCursor()
        cursor.execute(sqlText)
        resultList = cursor.fetchall()

        self.conn.close()

        return resultList
    
    def ExecNonQuery(self, sqlText):
        cur = self.__GetConnectCursor()
        cur.execute(sqlText)
        self.conn.commit()
        self.conn.close()

class DBA_Oracle:
    def __init__(self, DATA_SOURCE, USER_ID, PASSWORD):
        self.DATA_SOURCE = DATA_SOURCE
        self.USER_ID = USER_ID
        self.PASSWORD = PASSWORD
    
    def __GetConnectCursor(self):
        if not self.DATA_SOURCE:
            raise NameError("对不起，未设置数据库连接串信息！")
        
        self.conn = cx_Oracle.connect(user = self.USER_ID, password = self.PASSWORD, dsn = self.DATA_SOURCE, encoding = "UTF-8")
        cursor = self.conn.cursor()

        if not cursor:
            raise NameError("对不起，数据库连接失败!")
        else:
            return cursor
    
    def ExecQuery(self, sqlText):
        cursor = self.__GetConnectCursor()
        cursor.execute(sqlText)
        resultList = cursor.fetchall()

        self.conn.close()

        return resultList
    
    def ExecNonQuery(self, sqlText):
        cur = self.__GetConnectCursor()
        cur.execute(sqlText)
        self.conn.commit()
        self.conn.close()
