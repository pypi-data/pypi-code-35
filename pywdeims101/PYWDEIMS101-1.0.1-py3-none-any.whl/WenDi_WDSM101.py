import PYWDEIMS101.WenDi_WDDBA101 as wddba
import os 

class DBAccessHelper:

    @staticmethod
    def RunSQLReturnDataList(sqlText, databaseCode):
        varName = "PYSQL" + "_" + databaseCode
        dbSettingInfo = os.getenv(varName)
        if not dbSettingInfo:
            raise NameError("对不起，环境变量名为%s的信息未配置！" % (varName))

        lst_DBInfo = dbSettingInfo.split(";")
        db_enginee = lst_DBInfo[0]
        server = lst_DBInfo[1]
        user = lst_DBInfo[2]
        password = lst_DBInfo[3]
        db_name = ""
        if len(lst_DBInfo) > 4:
            db_name = lst_DBInfo[4]

        if db_enginee == "SQLSERVER":
            ms = wddba.DBA_SQLServer(server, db_name, user, password) 
            return ms.ExecQuery(sqlText)
        elif db_enginee == "MYSQL":
            ms = wddba.DBA_MySQL(server, db_name, user, password)
            return ms.ExecQuery(sqlText)
        elif db_enginee == "AZURESQL":
            ms = wddba.DBA_AzureSQL(server, db_name, user, password)
            return ms.ExecQuery(sqlText)
        elif db_enginee == "ORACLE":
            ms = wddba.DBA_Oracle(server, user, password)
            return ms.ExecQuery(sqlText)
        else:
            raise NameError("对不起，本系统暂不支持%s数据库引擎！" % (db_enginee))

    @staticmethod
    def RunSQL(sqlText, databaseCode):
        varName = "PYSQL" + "_" + databaseCode
        dbSettingInfo = os.getenv(varName)
        if not dbSettingInfo:
            raise NameError("对不起，环境变量名为%s的信息未配置！" % (varName))

        lst_DBInfo = dbSettingInfo.split(";")
        db_enginee = lst_DBInfo[0]
        server = lst_DBInfo[1]
        user = lst_DBInfo[2]
        password = lst_DBInfo[3]
        db_name = ""
        if len(lst_DBInfo) > 4:
            db_name = lst_DBInfo[4]

        if db_enginee == "SQLSERVER":
            ms = wddba.DBA_SQLServer(server, db_name, user, password) 
            ms.ExecNonQuery(sqlText)
        elif db_enginee == "MYSQL":
            ms = wddba.DBA_MySQL(server, db_name, user, password)
            ms.ExecNonQuery(sqlText)
        elif db_enginee == "AZURESQL":
            ms = wddba.DBA_AzureSQL(server, db_name, user, password)
            ms.ExecNonQuery(sqlText)
        elif db_enginee == "ORACLE":
            ms = wddba.DBA_Oracle(server, user, password)
            return ms.ExecNonQuery(sqlText)
        else:
            raise NameError("对不起，本系统暂不支持%s数据库引擎！" % (db_enginee))


