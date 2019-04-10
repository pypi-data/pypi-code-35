r"""
    All sql put in this pool.
    Send sql-token to get sql string.
"""
import os
import datetime
from time import strftime, localtime
from configparser import ConfigParser
import re


conf = ConfigParser()
home_dir = os.path.dirname(os.path.realpath(__file__))
conf_path = os.path.join(home_dir, "config.conf")
conf.read(conf_path)

year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min_ = strftime("%M", localtime())
sec = strftime("%S", localtime())
v_date = datetime.datetime.now().strftime('%Y-%m-%d')


def sql_change(sql_path, sql_token):
    r"""
    get sql change
    :param sql_path:
    :param sql_token:
    :return:
    """
    sql_file_name = sql_token
    sql_file_path = os.path.join(sql_path, sql_file_name)

    try:
        fpo = open(sql_file_path, 'r', encoding='utf8')
    except Exception:
        fpo = open(sql_file_path, 'r', encoding='gbk')

    output_string = ''

    try:
        sql_string = fpo.readlines()
        for ele in sql_string:
            output_string += ele.replace('\n', ' ')
    except Exception:
        pass
    finally:
        fpo.close()

    return output_string


def proc_get(proc_name, schema, param):
    r"""
    get proc run sql
    :param proc_name:
    :param schema:
    :param param:
    :return:
    """
    output = "begin     " + schema + "." + proc_name
    params = ""
    lastindex = len(param) - 1
    if proc_name[0:3] == 'EAS':
        if param:
            params += "("
            for i in param:
                if param.index(i) != lastindex:
                    params += "'" + str(i) + "',"
                else:
                    params += "'" + str(i) + "')"
    elif proc_name == 'rtl_rp_seperate':
        if param:
            params += "("
            for i in param:
                if param.index(i) != lastindex:
                    params += "'" + str(i) + "',"
                else:
                    params += "'" + str(i) + "')"
    else:
        formats = 'yyyy-MM-dd'
        if param:
            params += "("
            for i in param:
                if param.index(i) != lastindex:
                    params += "to_date('" + str(i) + "','" + formats + "'),"
                else:
                    params += "to_date('" + str(i) + "','" + formats + "'))"
    output = output + params + ";  end;"
    return output


def get_firstday_of_month():
    r"""
        get the first day of month
        date format = "YYYY-MM-DD"
    """
    year_ = strftime("%Y", localtime())
    mon_ = strftime("%m", localtime())
    days = "01"
    if int(mon) < 10:
        mon_ = "0"+str(int(mon_))
    arr = (year_, mon_, days)
    return "-".join("%s" % i for i in arr)


def is_monthend():
    r"""
    is or not monthend
    :return:
    """
    date = v_date
    print(date)
    if date == get_firstday_of_month():
        return "is_month_end"
    else:
        return "not_month_end"


def return_sql(sql_path, sql_name, need_chinese=True):
    r"""
    return sql list
    :param sql_path:
    :param sql_name:
    :param need_chinese:
    :return:
    """

    sql_file_name = sql_name
    sql_file_path = os.path.join(sql_path, sql_file_name)

    try:
        fpo = open(sql_file_path, 'r', encoding='utf-8')
        sql_string = fpo.readlines()
    except Exception:
        fpo = open(sql_file_path, 'r', encoding='gbk')
        sql_string = fpo.readlines()

    for i in sql_string:
        if '--' in i:
            index = sql_string.index(i)
            sql_string[index] = ""
        else:
            pass
    output_string = ''

    try:
        for ele in sql_string:
            output_string += ele.replace('\n', ' ')
    except Exception:
        pass
    finally:
        fpo.close()

    if not need_chinese:
        # 将sql中的中文替换成''
        output_string = re.sub(r'[\u4e00-\u9fa5]', '', output_string)
        # 将sql中的中文字符替换成''
        output_string = re.sub(r'[^\x00-\x7f]', '', output_string)

    list_ = output_string.split(";")
    for i in list_:
        if i.strip() == '':
            list_.remove(i)

    return list_