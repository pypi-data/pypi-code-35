#coding=utf8
import socket
import sys
import datetime
import configparser as ConfigParser
import urllib3
import os
import csv
import time
import sqlite3

remote_ip=''
port=0
RECBUFFER=0
SNDBUFFER=0
DIRNAME=os.path.dirname(os.path.realpath(__file__))

try:
    conn = sqlite3.connect('/data/lhjy/sqlite/tmpfs/StockData.db')
    cursor = conn.cursor()
except Exception as e:
    print (e)

try:
    config = ConfigParser.ConfigParser()
    # f = open(DIRNAME + '/client.ini.py', "rb")
    config.read(DIRNAME + '/client.ini.py')
    remote_ip = config.get("server", "IP")
    port = config.get("server", "PORT")
except Exception as e:
    print (e)
    print ('Read config file ERROR! (\"client.ini.py\")')
    sys.exit()
#返回与server端的连接s
def GetConnection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print ('Failed to create socket. Error code: ' + str(e))
        sys.exit()
    # print 'Socket Created'
    try:
        global remote_ip
        global port
        global RECBUFFER
        global SNDBUFFER
        config = ConfigParser.ConfigParser()
        config.readfp(open(DIRNAME+'/client.ini.py', "rb"))
        remote_ip=config.get("server", "IP")
        port=int(config.get("server", "PORT"))
        RECBUFFER = int(config.get("client", "RECBUFFER"))
        SNDBUFFER = int(config.get("client", "SNDBUFFER"))
    except Exception as e:
        print (e)
        print ('Read config file ERROR! (\"client.ini.py\")')
        sys.exit()
    s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SNDBUFFER)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECBUFFER)
    s.connect((remote_ip, port))
    # print 'Socket Connected to '+ remote_ip
    return s

def QueryRequest(rname,arg,max_retry=10, time_out=5):
    args=[rname]+arg
    str_sql=''
    for i in range(len(args)):
        args[i]=str(args[i])
    if args[0] == 'GetStkPrice' and args.__len__()==4:
        str_sql = 'select * from tb_st22047_parq where obj=\"' + args[1] + '\" and timing>=' + args[2] + ' and timing<=' + args[3]+' order by timing'
    elif args[0]=='GetStkEx'and args.__len__()==2:
        str_sql = 'select * from tb_st22041_parq where obj=\"' + args[1]+'\"'
    elif args[0]=='GetStkName'and args.__len__()==2:
        str_sql = 'select * from tb_st32_parq where obj=\"' + args[1] + '\"'
    elif args[0]=='GetInxPrice'and args.__len__()==4:
        str_sql = 'select * from tb_st22157_parq where obj=\"' + args[1] + '\" and timing>=' + args[2] + ' and timing<=' + args[3] +' order by timing'
    elif args[0]== 'GetL2Data' and args.__len__()==2:
        str_sql='select * from tb_stl2 where obj=\"'+args[1]+'\" order by t_day,t_time'
    elif args[0]=='GetStkCode' and args.__len__()==1:
        str_sql='select distinct obj from tb_stl2 order by obj'
    elif args[0]=='GetStkCodeST22047' and args.__len__()==1:
        str_sql='select distinct obj from tb_st22047_parq order by obj'
    elif args[0]=='GetAllBK' and args.__len__()==1:
        str_sql='select * from tb_bkCode_parq where timing = (select max(timing) from tb_bkCode_parq)'
    elif args[0]=='GetAllBKByTime' and args.__len__()==2:
        str_sql='select * from tb_bkCode_parq where timing = '+args[1]
    elif args[0]=='GetBKByStk' and args.__len__()==2:
        str_sql='select * from tb_bkCode_parq where timing = (select max(timing) from tb_bkCode_parq) and code in (select distinct(bkCode) from tb_bkStock_parq where timing=(select max(timing) from tb_bkStock_parq) and stkCode=\"'+args[1] +  '\")'
    elif args[0]=='GetBKByStkTime' and args.__len__()==3:
        str_sql='select * from tb_bkCode_parq where timing = '+args[2]+' and code in (select distinct(bkCode) from tb_bkStock_parq where timing='+args[2]+' and stkCode=\"'+args[1] +  '\")'
    elif args[0]=='GetBKByName' and args.__len__()==2:
        str_sql='select * from tb_bkCode_parq where timing = (select max(timing) from tb_bkCode_parq) and name=\"' + args[1] +'\"'
    elif args[0]=='GetBKByNameTime' and args.__len__()==3:
        str_sql='select * from tb_bkCode_parq where timing = '+args[2] +' and name=\"' + args[1] +'\"'
    elif args[0] == 'GetBKByCode' and args.__len__() == 2:
        str_sql = 'select * from tb_bkCode_parq where timing = (select max(timing) from tb_bkCode_parq) and code=\"' + args[1] + '\"'
    elif args[0]=='GetBKByCodeTime' and args.__len__()==3:
        str_sql='select * from tb_bkCode_parq where timing = '+args[2] +' and code=\"' + args[1] +'\"'
    elif args[0]=='GetStkByBKCode' and args.__len__() == 2:
        str_sql = 'select * from tb_bkStock_parq where timing =  (select max(timing) from tb_bkStock_parq) and bkCode=\"' + args[1] + '\"'
    elif args[0]=='GetStkByBKCodeTime' and args.__len__() == 3:
        str_sql = 'select * from tb_bkStock_parq where timing =  '+args[2] +' and bkCode=\"' + args[1] + '\"'
    elif args[0]=='GetStkPriceAll' and args.__len__() == 3:
        str_sql = 'select * from tb_st22047_parq where timing>= '+args[1]+' and timing <='+args[2]+' order by obj,timing'
    elif args[0]=='GetStkPriceAllEx' and args.__len__() == 3:
        str_sql = 'select * from tb_st22047_ex where timing>= '+args[1]+' and timing <='+args[2]+' order by obj,timing'
    elif args[0]=='GetStkPriceGroup' and args.__len__() == 4:
        str_sql = 'select * from tb_st22047_parq where obj in ('+args[1]+ ') and timing>= '+args[2]+' and timing <='+args[3]+' order by obj,timing'
    elif args[0] == 'GetStkPriceGroupEx' and args.__len__() == 4:
        str_sql = 'select * from tb_st22047_ex where obj in (' + args[1] + ') and timing>= ' + args[
            2] + ' and timing <=' + args[3] +' order by obj,timing'
    elif args[0] == 'GetStkPriceEx' and args.__len__()==4:
        str_sql = 'select * from tb_st22047_ex where obj=\"' + args[1] + '\" and timing>=' + args[2] + ' and timing<=' + args[3]+' order by timing'
    elif args[0]=='DoSQL' and args.__len__()==2:
        str_sql=args[1]
    data=[]
    try:
        cursor.execute(str_sql)
        data=cursor.fetchall()
    except Exception as e:
        print(e)
    res = [list(i) for i in data]
    if args[0]=='GetStkCodeST22047':
        for i in range(len(res)):
            res[i]=res[i][0]
    return res

#给定股票代码、时间区间，返回查询结果，ex参数表示是否动态复权，re表示是否复权
def GetStkPrice(stkcode,starttime,endtime,ex=False,re=True,timeout=10):
    if ex==True or re==False:
        res = QueryRequest('GetStkPrice', [stkcode, starttime, endtime], time_out=timeout)
        # del_list = []
        # for i in range(res.__len__()):
        #     if float(res[i][2]) == 0:
        #         del_list.append(i)
        # for i in reversed(del_list):
        #     del (res[i])
        if ex==True:
            cursor.execute('select * from tb_st22041_parq where obj=\'%s\' order by c1 desc' % (stkcode))
            tmp = cursor.fetchall()
            ex_res = [list(i) for i in tmp]
            # ex等于True时把结束时间以后的复权因子删除
            if ex_res.__len__()>0:
                res = do_ex(res, ex_res, ex)
    else:
        res = QueryRequest('GetStkPriceEx', [stkcode, starttime, endtime], time_out=timeout)
    return res

def GetStkPrice_old(stkcode,starttime,endtime,ex=False,re=True):
    res=QueryRequest('GetStkPrice',[stkcode,starttime,endtime])
    del_list=[]
    for i in range(res.__len__()):
        if float(res[i][2])==0:
            del_list.append(i)
    for i in reversed(del_list):
        del(res[i])
    #请求复权因子数据
    # time.sleep(0.2)
    ex_res = QueryRequest('GetStkEx', [stkcode])
    # ex等于True时把结束时间以后的复权因子删除
    if ex_res.__len__()==0 or re==False: return res
    if ex==True:
        for index,value in enumerate(ex_res):
            if int(value[1])>endtime:
                ex_res=ex_res[:index]
                break
    # 进行复权计算
    if ex_res.__len__()==0: return res
    for i in range(res.__len__()):

        if res[i][1] >= ex_res[0][1]:
            break
        # for ex_line in reversed(ex_res):
        for ex_line in ex_res:
            if ex_line[1] > res[i][1]:
                for j in range(4):
                    res[i][2 + j] = str(((float(res[i][2 + j]) - float(ex_line[2])) / (1 + float(ex_line[3]))))
                res[i][6]=str(float(res[i][6])*(1 + float(ex_line[3])))
            # else:
            #     break
    return res

def do_ex(stockdata,exdata,dy_ex=True):
    res=stockdata[:]
    if len(stockdata)==0: return res
    endtime=int(stockdata[-1][1])
    if dy_ex==True:
        for index,value in enumerate(exdata):
            if int(value[1])>endtime:
                exdata=exdata[:index]
                break
    # 进行复权计算
    if exdata.__len__()==0: return stockdata
    for i in range(res.__len__()):

        if res[i][1] >= exdata[0][1]:
            break
        # for ex_line in reversed(ex_res):
        for ex_line in exdata:
            if ex_line[1] > res[i][1]:
                for j in range(4):
                    res[i][2 + j] = str(((float(res[i][2 + j]) - float(ex_line[2])) / (1 + float(ex_line[3]))))
                res[i][6]=str(float(res[i][6])*(1 + float(ex_line[3])))
            # else:
            #     break
    return res

#给定股票代码，获取除权信息
def GetStkEx(stkcode):
    res=QueryRequest('GetStkEx', [stkcode])
    return res

#给定股指代码、时间区间，返回查询结果
def GetInxPrice(inxcode,starttime,endtime):
    return QueryRequest('GetInxPrice', [inxcode, starttime, endtime])

#给定代码，返回中文名称
def GetStkName(stkcode):
    return QueryRequest('GetStkName', [stkcode])

def GetStkCodeST22047():
    return QueryRequest('GetStkCodeST22047',[])

def GetAllBK():
    return QueryRequest('GetAllBK',[])

def GetBKByName(name):
    return QueryRequest('GetBKByName',[name])

def GetBKByNameTime(name,time):
    return QueryRequest('GetBKByNameTime',[name,time])

def GetBKByCode(code):
    return QueryRequest('GetBKByCode',[code])

def GetBKByCodeTime(code,time):
    return QueryRequest('GetBKByCodeTime',[code,time])

def GetStkByBKCode(code):
    return QueryRequest('GetStkByBKCode',[code])

def GetStkByBKCodeTime(code,time):
    return QueryRequest('GetStkByBKCodeTime',[code,time])

def DoSQL(sql,timeout=10):
    return QueryRequest('DoSQL',[sql])


def GetL2Data(stkcode):
    qres= QueryRequest('GetL2Data',[stkcode])
    tmps=[]
    for line in qres:
        try:
            tmp = []
            tmp.append(line[0])
            tmp.append(float(line[1]))
            if tmp[-1] == 0.0: continue
            tmp.append(float(line[2]))
            tmp.append(float(line[3]))
            tmp.append(float(line[4]))
            tmp.append(float(line[5]))
            tmp.append(float(line[6]))
            tmp.append(float(line[7]))
            tmp.append(float(line[8]))
            tmp.append(float(line[9]))
            tmp.append(int(line[10]))
            tmp.append(float(line[11]))
            tmp.append(int(line[12]))
            tmp.append(float(line[13]))
            tmp.append(int(line[14]))
            tmp.append(float(line[15]))
            tmp.append(int(line[16]))
            tmp.append(float(line[17]))
            tmp.append(int(line[18]))
            tmp.append(float(line[19]))
            tmp.append(int(line[20]))
            tmp.append(float(line[21]))
            tmp.append(int(line[22]))
            tmp.append(float(line[23]))
            tmp.append(int(line[24]))
            tmp.append(float(line[25]))
            tmp.append(int(line[26]))
            tmp.append(float(line[27]))
            tmp.append(int(line[28]))
            tmp.append(float(line[29]))
            tmp.append(int(line[30][0:4])*10000000000+int(line[30][5:7])*100000000+int(line[30][8:10])*1000000+int(line[31][0:2])*10000+int(line[31][3:5])*100+int(line[31][6:8])*1)
            tmps.append(tmp)
        except Exception as e:
            print (e)
            print (line)
        #print tmp
    return tmps

def GetStkCode():
    return QueryRequest('GetStkCode',[])



# codes= GetStkCode()
def GetTimeStr(daytime,ttime=-1,template='--::'):
    if ttime==-1:
        year=str(daytime/10000000000)
        month=str((daytime%10000000000)/100000000)
        day=str((daytime%100000000)/1000000)
        hour=str((daytime%1000000)/10000)
        minute=str((daytime%10000)/100)
        second=str(daytime%100)
    else:
        year = str(daytime / 10000)
        month = str((daytime % 10000) / 100)
        day = str((daytime % 100) / 1)
        hour = str(ttime / 10000)
        minute = str((ttime % 10000) / 100)
        second = str(ttime % 100)
    if month.__len__() == 1: month = '0' + month
    if day.__len__() == 1: day = '0' + day
    if hour.__len__() == 1: hour = '0' + hour
    if minute.__len__() == 1: minute = '0' + minute
    if second.__len__() == 1: second = '0' + second
    str1 = year + template[0] + month + template[1] + day
    str2 = hour + template[2] + minute + template[3] + second
    return {'day': str1, 'time': str2}



#给定股票代码、时间区间，返回查询结果，ex参数表示是否动态复权，re表示是否复权
def downloadStkPrice(stkcode,starttime,endtime,ex=False,re=True):
    res=QueryRequest('GetStkPrice',[stkcode,starttime,endtime])
    del_list=[]
    for i in range(res.__len__()):
        if float(res[i][2])==0:
            del_list.append(i)
    for i in reversed(del_list):
        del(res[i])
    #请求复权因子数据
    ex_res = QueryRequest('GetStkEx', [stkcode])
    # ex等于True时把结束时间以后的复权因子删除
    if ex_res.__len__()==0 or re==False:
        csv.writer(open('localData/' + stkcode.replace('.stk', '.csv'), 'wb')).writerows(res)
        return res
    if ex==True:
        for index,value in enumerate(ex_res):
            if int(value[1])>endtime:
                ex_res=ex_res[:index]
                break
    # 进行复权计算
    if ex_res.__len__()==0:
        csv.writer(open('localData/' + stkcode.replace('.stk', '.csv'), 'wb')).writerows(res)
        return res
    for i in range(res.__len__()):

        if res[i][1] >= ex_res[0][1]:
            break
        # for ex_line in reversed(ex_res):
        for ex_line in ex_res:
            if ex_line[1] > res[i][1]:
                for j in range(4):
                    res[i][2 + j] = str(((float(res[i][2 + j]) - float(ex_line[2])) / (1 + float(ex_line[3]))))
                res[i][6]=str(float(res[i][6])*(1 + float(ex_line[3])))
            # else:
            #     break

    csv.writer(open('localData/'+stkcode.replace('.stk','.csv'),'wb')).writerows(res)
    return res

def getStkPriceLocal(stkcode,starttime,endtime):
    res=list(csv.reader(open('localData/'+stkcode.replace('.stk','.csv'),'rb')))
    start=0
    for i in range(len(res)):
        if int(res[i][1])>=int(starttime):
            start=i
            break
    end=len(res)
    for i in range(len(res)):
        if int(res[i][1])>int(endtime):
            end=i
            break
    return res[start:end]



def get_day_type(query_date):
    url = 'http://10.60.103.246:25566/' + query_date
    max_retry=10
    count=0
    while(count<max_retry):
        try:
            resp = urllib3.urlopen(url, timeout=5)
            content=resp.read()
            count = 999999
        except Exception as e:
            print (e)
    # print type(content)
    if content=="0":
        try:
            day_type = int(content)
        except ValueError:
            return -1
        else:
            return day_type
    else:
        return -1

# 把2维list组成的多支股票数据转化为字典
def ListDataToDict(lines):
    res = {}
    i = 0
    linecount = len(lines)
    while (i < linecount):
        tmp = [lines[i]]
        while (i + 1 < linecount and lines[i][0] == lines[i + 1][0]):
            i += 1
            tmp.append(lines[i])
        res[tmp[0][0]] = tmp
        i += 1
    return res

# 获取stime到etime所有股票的数据，组成字典返回
def GetStkPriceAll(stime,etime=99999999999999,ex=True):
    if ex==False:
        cursor.execute('select * from tb_st22047_parq where timing>=%d and timing<=%d order by obj,timing' % (stime,etime))
        tmp = cursor.fetchall()
        lines = [list(i) for i in tmp]
    else:
        cursor.execute(
            'select * from tb_st22047_ex where timing>=%d and timing<=%d order by obj,timing' % (stime, etime))
        tmp = cursor.fetchall()
        lines = [list(i) for i in tmp]

    res=ListDataToDict(lines)
    return res

# 获取stklist数组中股票代码的一段时间内数据，组成字典返回
def GetStkPriceGroup(stklist,stime,etime=99999999999999,ex=True):
    stkcodes=""
    for line in stklist:
        stkcodes+=('\''+line+'\',')
    stkcodes=stkcodes[:-1]
    if ex==False:
        cursor.execute(
            'select * from tb_st22047_parq where obj in (%s) and timing>=%d and timing<=%d order by obj,timing' % (stkcodes, stime, etime))
        tmp = cursor.fetchall()
        lines = [list(i) for i in tmp]
        #lines = QueryRequest('GetStkPriceGroup',[stkcodes,stime,etime],time_out=3600)
    else:
        cursor.execute(
            'select * from tb_st22047_ex where obj in (%s) and timing>=%d and timing<=%d order by obj,timing' % (
            stkcodes, stime, etime))
        tmp = cursor.fetchall()
        lines = [list(i) for i in tmp]
        #lines = QueryRequest('GetStkPriceGroupEx',[stkcodes,stime,etime],time_out=3600)
    res=ListDataToDict(lines)
    return res

def is_tradeday(query_date):
    weekday = datetime.datetime.strptime(query_date, '%Y%m%d').isoweekday()
    if weekday <= 5 and get_day_type(query_date) == 0:
        return 1
    else:
        return 0


def today_is_tradeday():
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)

if __name__=="__main__":
    #print getStkPriceLocal('SH600000.stk',0,19991112000000)
    # print time.strftime('%H:%M:%S')
    # res= GetStkPriceAll(20180101000000)
    # print time.strftime('%H:%M:%S')
    # print DoSQL('select * from tb_st22047_parq order by timing limit 10')
    # print res
    # print GetStkPrice('SH600000.stk', 20100000000000,20110000000000,ex=True)
    # print GetStkPrice_old('SH600000.stk', 20100000000000,20110000000000,ex=False)
    code=GetBKByName('HS300_')[0][0]
    stkcodes=[]
    for line in GetStkByBKCode(code):
        stkcodes.append(line[1])
    for i,code in enumerate(stkcodes):
        print (i)
        t= GetStkPrice(code,2018010100000,20180801000000,ex=False,re=False)


    #print res


#
# res= GetStkPrice('SH600050.stk',20100000000000,20170401000000,True)
# for line in res:
#     print line
#
# print GetStkName('SH000300.index')




