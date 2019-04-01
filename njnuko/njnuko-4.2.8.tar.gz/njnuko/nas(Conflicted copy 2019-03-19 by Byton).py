import os
import os.path
import shutil
import time
import datetime
import stat
from PIL import Image,ImageFile
from PIL import ImageChops
from PIL.ExifTags import TAGS
import locale
import filetype
import hashlib
import pymysql
import time
import psycopg2
import csv
import sqlite3
locale.getdefaultlocale()
import csv


checking = []
compare = []

################### Front Function ####################
def compare_files(folder,table,dblink):
    global compare
    compare = []
    log = os.path.join(os.path.dirname(folder),'compare_files.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()  
    process_compare(folder,table,dblink,log)
    InsertData(os.path.basename(folder),log,dblink)

    return log
    
def process_compare(folder,table,dblink,log):

    for i in os.listdir(folder):
        
        if os.path.isdir(os.path.join(folder,i)):
            print(str(os.path.join(folder,i))+ " is directory")
            if i[0] not in ['@','.']:
                print(str(os.path.join(folder,i)) + " is not dummy folder")
                process_compare(os.path.join(folder,i),table,dblink,log)
        else:
            hash = ''
            the_md5=hashlib.md5()
            with open(os.path.join(folder,i), 'rb') as f:
                the_md5.update(f.read())
                hash = the_md5.hexdigest()
            if hash in compare:
                with open(log,'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['duplicate',os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])

                os.remove(os.path.join(folder,i)) 
            else:
                a = GetData(table,hash,dblink)
                if a is not None:

                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['compare',os.path.join(folder,i),a[1],os.path.getsize(os.path.join(folder,i)),hash])
                    os.remove(os.path.join(folder,i))
                else:
                     with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['new',os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])                   
                    
                compare.append(hash)                               






################### Front Function ####################

def check_files(folder,dblink):
    global checking
    checking = []
    log = os.path.join(os.path.dirname(folder),'check_files.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()  
    process_checking(folder,log)

    InsertData(os.path.basename(folder),log,dblink)
    return log
    
def process_checking(folder,log):
    global checking 
    for i in os.listdir(folder):
        
        if os.path.isdir(os.path.join(folder,i)):
            print(str(os.path.join(folder,i))+ " is directory")
            if i[0] not in ['@','.']:
                print(str(os.path.join(folder,i)) + " is not dummy folder")
                process_checking(os.path.join(folder,i),log)
        else:
            hash = ''
            the_md5=hashlib.md5()
            with open(os.path.join(folder,i), 'rb') as f:
                the_md5.update(f.read())
                hash = the_md5.hexdigest()
            if hash in checking:
                with open(log,'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['duplicate',os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                os.remove(os.path.join(folder,i)) 
            else:
                with open(log,'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['new',os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                checking.append(hash)         

################### Front Function ####################

            
def class_bysize(folder,dstfold,dblink,large=1048576):
    log = os.path.join(os.path.dirname(folder),'class_bysize.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()  
    process_bysize(folder,dstfold,log,large)

    InsertData(os.path.basename(folder),log,dblink)

def process_bysize(folder,dstfold,log,large):

    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bysize(os.path.join(folder,i),dstfold,log,large)
            else:
                size = os.path.getsize(os.path.join(folder,i))
                if size < large:
                    file_move(folder,i,dstfold,log)
                else:
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['new',os.path.join(folder,i),'',size,''])
                        f.close()     


################### Front Function ####################


################### Front Function ####################

            
def class_bytype(folder,dstfold,dblink):
    log = os.path.join(dstfold,'class_bytype.log')
    if os.path.exists(log):
        os.remove(log)


    f = open(log,'w')
    f.close()      
    process_bytype(folder,dstfold,log)

    InsertData(os.path.basename(folder),log,dblink)

def process_bytype(folder,dstfold,log):

    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bytype(os.path.join(folder,i),dstfold,log)
            else:
                if filetype.guess(os.path.join(folder,i)) is not None:
                    type = filetype.guess(os.path.join(folder,i)).extension
                    if not (os.path.exists(os.path.join(dstfold,type))):
                        os.makedirs(os.path.join(dstfold,type))
                    file_move(folder,i,os.path.join(dstfold,type),log)

                else:
                    type = 'None'
                    if not (os.path.exists(os.path.join(dstfold,type))):
                        os.makedirs(os.path.join(dstfold,type))
                    file_move(folder,i,os.path.join(dstfold,type),log)

################### Front Function ####################

def class_bytime(folder,desfold,dblink):
    log = os.path.join(desfold,'class_bytime.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()      
    process_bytime(folder,desfold,log)
    InsertData(os.path.basename(folder),log,dblink)


def process_bytime(folder,desfold,log):
    for i in os.listdir(folder):
        if i[0] not in ['@','.']:

            if os.path.isdir(os.path.join(folder,i)):
                process_bytime(os.path.join(folder,i),desfold,log)
            else:            
                a = gettime(os.path.join(folder,i))[0:7]
                if not os.path.exists(os.path.join(desfold,a)):
                    os.makedirs(os.path.join(desfold,a))
                file_move(folder,i,os.path.join(desfold,a),log)

################### Backend Function ####################








def getDB(a):
    if a == 1:
        conn = pymysql.connect(host='home.njnuko.top', port=33066, user='root', passwd='admin',db='nas_files')
    elif a == 0:
        conn =  conn = sqlite3.connect('nas_files.db')
    elif a == 2:
        conn = psycopg2.connect(host='njnuko.top', port=10220, user='ko', password='231231',database='nas_files')
    return conn


def InsertData(TableName,csvfile,dblink):
    try:
        conn = getDB(dblink)
        cur=conn.cursor()
        print("create connection OK")
        ###create table
        sql1 = "create table " + TableName + " (action varchar(20),source varchar(1000),dest varchar(1000),size varchar(50),md5 varchar(50));" 
        print(sql1)
        cur.execute(sql1)
        print("create table OK")

        f = open(csvfile, 'r',newline='')
        csvreader = csv.reader(f)
        list1 = list(csvreader)
        print("========================")
        print(list1)
        print("========================")
        sql = "insert into " + TableName + " values(%s,%s,%s,%s,%s);"

        cur.executemany(sql,list1)
        conn.commit()        
        cur.close()
        conn.close()
    except Exception as e:
      print("Insert Data Error," + e)


def GetData(TableName,md5,dblink):
    try:
        conn = getDB(dblink)
        cur=conn.cursor()
        print("create connection OK")
        ###create table
        sql1 = "select action,source,md5 from " + TableName + " where " + TableName + ".action = " + "'new' and " + TableName + ".md5 = " + "'" + md5+"'" + ";" 
        print(sql1)
        cur.execute(sql1)
        print("create table OK")
        return cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
      print("Get Data Error," + e)


def file_move(frfolder,file1,dest,log):

    if os.path.exists(os.path.join(dest,file1)):
        the_md5=hashlib.md5()
        f1 = open(os.path.join(frfolder,file1), 'rb')
        the_md5.update(f1.read())
        hash1 = the_md5.hexdigest()
        f2 = open(os.path.join(dest,file1), 'rb')
        the_md5.update(f2.read())
        hash2 = the_md5.hexdigest()
        f1.close()
        f2.close()

        if hash1 == hash2:
            with open(log,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['delete',os.path.join(frfolder,file1),os.path.join(dest,file1),os.path.getsize(os.path.join(frfolder,file1)),hash1])
                f.close()
            os.remove(os.path.join(frfolder,file1))
        else:
            serialnumber = 1
            while os.path.exists(os.path.join(dest,os.path.splitext(file1)[0] + '-' + str(serialnumber) + os.path.splitext(file1)[1])):
                serialnumber = serialnumber + 1
            newfile = os.path.splitext(file1)[0] + '-'+ str(serialnumber) + os.path.splitext(file1)[1] 
 
            with open(log,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['rename',os.path.join(frfolder,file1),os.path.join(dest,newfile),os.path.getsize(os.path.join(frfolder,file1)),hash1])
                f.close()
            shutil.move(os.path.join(frfolder,file1),os.path.join(dest,newfile))
   


    else:
        the_md5=hashlib.md5()
        f1 = open(os.path.join(frfolder,file1), 'rb')
        the_md5.update(f1.read())
        hash1 = the_md5.hexdigest()
        f1.close()
        
        with open(log,'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['move',os.path.join(frfolder,file1),os.path.join(dest,file1),os.path.getsize(os.path.join(frfolder,file1)),hash1])
            f.close()
        shutil.move(os.path.join(frfolder,file1),dest)






def gettime(file):
    """Get embedded EXIF data from image file."""
    ret = {}
    if filetype.guess(file) is not None:
        if filetype.guess(file).extension in ('jpg','jpeg','gif','png','bmp'):    
            try:
                img = Image.open(file)
                if hasattr( img, '_getexif' ):
                    try:
                        exifinfo = img._getexif()
                    except:
                        exifinfo = None
                    if exifinfo != None:
                        for tag, value in exifinfo.items():
                            decoded = TAGS.get(tag, tag)
                            ret[decoded] = value
                    else:
                        timeArray = time.localtime(os.path.getctime(file))
                        otherStyleTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray)
                        return str(otherStyleTime).replace(':','-').replace(' ','_')
            except IOError:
                print('IOERROR/ValueError ' + file)


            
    if ret.get('DateTimeOriginal') != None:
        cd = ret.get('DateTimeOriginal')[0:7].replace(':','-').replace(' ','')
        return cd
    else:
        timeArray = time.localtime(os.path.getctime(file))
        otherStyleTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray)
        return str(otherStyleTime).replace(':','-').replace(' ','_')
#        print('creation date: '+os.path.getctime(fname).replace(':','-').replace(' ','_') ) 
#        return os.path.getctime(fname).replace(':','-').replace(' ','_')   



def get_size(file):
    return os.path.getsize(file)


def main():
    pass
if __name__ == '__main__':
    main()
