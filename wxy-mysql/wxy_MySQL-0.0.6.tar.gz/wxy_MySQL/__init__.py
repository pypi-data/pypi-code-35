import pymysql


# sql语句使用三引号('''.......''')标注
# 方法中参数 sql 为True时，调用方法的同事会输出sql语句，方便调试




class MySQLdb:

    # 初始化连接数据库
    def __init__(self,db_host,user,password,db_name):

        self.db=pymysql.connect(db_host,user,password,db_name)   # 先建立数据库连接
        self.cursor=self.db.cursor()                             # 在连接基础上创建游标

    # 建表
    def create_table(self,t_name,dictionary,override=False,sql=False):
        '''
            默认表字段Null属性为true
            传入字典形式的key:type值
        '''
        if isinstance(dictionary,dict) is False:
            raise Exception("请传入字典形式的conditions")

        if override == True:
            sql_delete_table = """drop table if exists {};""".format(t_name)  # 若表存在，则覆盖
            if sql == True:
                print(sql_delete_table)
            self.cursor.execute(sql_delete_table)

        list_key=list(dictionary.keys())
        list_value=list(dictionary.values())

        table_structure = []
        for i in range(len(list_key)):
            single_str=str(list_key[i])+' '+str(list_value[i])
            table_structure.append(single_str)
        sql_create_table="""create table {} ({});""".format(t_name,','.join(table_structure))
        if sql==True:
            print(sql_create_table)
        self.cursor.execute(sql_create_table)

    # 删表
    def drop_table(self,t_name,sql=False):

        sql_drop_table="""drop table if exists {};""".format(t_name)
        if sql==True:
            print(sql_drop_table)
        self.cursor.execute(sql_drop_table)

    # 查
    def select(self,t_name,select_what,conditions=None,sql=False):
        '''
        返回结果列表，若查无结果，则返回空列表
        '''

        if isinstance(select_what,str) is False:
            raise Exception('请传入字符串形式的select_what')

        if conditions==None:
            sql_select = """select {} from {};""".format(select_what,t_name)
            if sql==True:
                print(sql_select)
            self.cursor.execute(sql_select)
            result_tuple=self.cursor.fetchall()
            result_list=[]
            for i in result_tuple:
                result_list.append(str(i[0]).replace(',',''))

            return result_list

        else:
            if isinstance(conditions,str) is False:
                raise Exception('请传入字符串形式的conditions')
            else:
                sql_select = """select {} from {} where {};""".format(select_what,t_name,conditions)
                if sql ==True:
                    print(sql_select)
                self.cursor.execute(sql_select)
                result_tuple = self.cursor.fetchall()
                print(result_tuple)
                result_list = []
                for i in result_tuple:
                    result_list.append(i[0])

                return result_list

    # 增
    def insert(self,t_name,dictionary,sql=False):

        # 判断传入参数是否为dict
        if isinstance(dictionary,dict) is not True:
            raise Exception("请输入字典形式的dictionary")

        list_key=list(dictionary.keys())
        list_value=list(dictionary.values())
        key=','.join(list_key)
        # key直接进行字符串拼接，嵌入sql中;value直接嵌入列表，然后将[]去掉
        sql_insert_into="""insert into {} ({}) values ({});""".format(t_name,key,list_value).replace('[','').replace(']','')
        if sql == True:
            print(sql_insert_into)
        self.cursor.execute(sql_insert_into)
        self.db.commit()

    # 改
    def update(self,t_name,dictionary,conditions,sql=False):

        # conditions 必须传入list
        if isinstance(conditions, str) is False:
            raise Exception('请传入字符串形式的conditions')

        # dictionary 必须传入dict
        if isinstance(dictionary,dict) is False:
            raise Exception('请传入字典形式的dictionary')

        list_key = list(dictionary.keys())
        list_value = list(dictionary.values())

        update = '' # 创建一个空字符串，用来储存拼接字符串
        for i in range(len(list_key)):
            # global string

            # 如果要update的值为数字
            if isinstance(list_value[i],int) or isinstance(list_value[i],float) is True:
                string = list_key[i] + '=' + str(list_value[i])+','

            elif isinstance(list_value[i], str) is True:
                # 若字符串中含有单引号(')
                if "'" in list_value[i] is True:
                    string = list_key[i] + '=' + '"' + list_value[i] + '"' + ','
                elif '"' in list_value[i] is True:
                    string = list_key[i] + '=' + "'" + list_value[i] + "'" + ','
                else:
                    string = list_key[i] + '=' + "'" + list_value[i] + "'" + ','
            else:
                raise Exception('还未能判断string、digital外的类型')

            update=update+string

        update=update.rstrip(',')

        sql_update = """update {} set {} where {};""".format(t_name,update,conditions)
        if sql == True:
            print(sql_update)
        self.cursor.execute(sql_update)
        self.db.commit()

    # 删
    def delete(self,t_name,conditions,sql=False):

        if conditions == None:   # 清空整张表
            sql_delete = """delete from {};""".format(t_name)
            if sql == True:
                print(sql_delete)
            self.cursor.execute(sql_delete)
            self.db.commit()
        else:
            if isinstance(conditions,str) is False:
                raise Exception('请传入字符串形式的conditions')
            sql_delete = """delete from {} where {};""".format(t_name,conditions)
            if sql == True:
                print(sql_delete)
            self.cursor.execute(sql_delete)
            self.db.commit()

    # 查重
    # def select_repeat(self):
    #
    #     sql_select_repeat='''select {所有} from {表名} where {字段} in (select {字段} from {表名} group by {} having count({})>1);'''
