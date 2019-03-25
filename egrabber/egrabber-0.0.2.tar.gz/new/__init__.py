import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup
import bleach
import urllib.request
import sqlite3
import xlwt 
from xlwt import Workbook 
import xlrd 

class project:

    def __init__(self):
        conn = sqlite3.connect('sam2.db')
        c = conn.cursor()
        self.c=c
        wb = Workbook() 
        self.wb=wb 

    def strip_html(self,html_str):
        tags = []
        attr = {}
        styles = []
        strip = True
        return bleach.clean(html_str,tags=tags,attributes=attr,styles=styles,strip=strip)


    def create_DB(self):
        self.c.execute('create table sheet1 (name varchar[15] , Count int);')
        

    def insert_DB(self,word,wordcount):
        self.c.execute('INSERT INTO sheet1 (name,Count) VALUES (?, ?)',(word,wordcount))    
        
    def Get_DB(self):
        p1=[]
        l=[]
        p=self.c.execute('select * from sheet1')
        data = p.fetchall()
        #print(data)
        for a, b in data:
            l.append(str(b))
            p1.append(str(a))
        return l,p1
    
    def __del__(self):
        self.c.close()

    def download(self):
        response = urllib.request.urlopen('http://www.yellowpages.com')
        html = response.read()
        #html=self.strip_html(html)
        soup = BeautifulSoup(html, 'html.parser')
        l=soup.find_all('p')
        #l1=soup.find_all('h1)
        wholetext=''
        for sub_heading in l:
            wholetext=wholetext+sub_heading.text
        return wholetext

    # def count_word(self,word,content):
    #     return contents.Count(word)

    def W_excel(self):
        sheet1 = self.wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'http://www.google.com') 
        sheet1.write(1, 0, 'and') 
        sheet1.write(2, 0, 'is') 
        sheet1.write(3, 0, 'if')
        self.wb.save("sample.xls") 
    
    def R_excel(self):
        wb = xlrd.open_workbook('sample.xls')
        rword=[]
        rw_count=[]
        sheet = wb.sheet_by_index(0)
        for i in range(sheet.nrows): 
            print(sheet.cell_value(i, 0)) 
        

ob=project()

#ob.create_DB()
ob.insert_DB('and',50)
ob.insert_DB('is',60)
ob.W_excel()
ob.Get_DB()
#parsedhtml= ob.download()
#del ob

