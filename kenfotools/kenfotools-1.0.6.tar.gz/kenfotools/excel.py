import os
import xlrd
import xlwt
from xlutils.copy import copy

"""
excel to list 

like that:
[{'field1':1,'field2':2},{'field1':2,'field2':3}]
"""
def tolist(filename):
    result = []
    if os.path.exists(filename):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        row_num, clo_num = sheet.nrows, sheet.ncols
        field = sheet.row_values(0)
        for row in range(1, row_num):
            obj = {}
            data = sheet.row_values(row)
            for i in range(clo_num):
                obj[field[i]] = data[i]
            result.append(obj)
    return result



def read_field(filename):
    if os.path.exists(filename):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        field = sheet.row_values(0)
        return field


"""
read excel by line
"""
def read_line(filename, func):
    if os.path.exists(filename):
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        row_num, clo_num = sheet.nrows, sheet.ncols
        field = sheet.row_values(0)
        for row in range(1, row_num):
            obj = {}
            data = sheet.row_values(row)
            for i in range(clo_num):
                obj[field[i]] = data[i]
            func(obj)


"""
Writer list to Excel

data like that:
data=[{'field1':1,'field2':2},{'field1':2,'field2':3}]
"""
def write(excel_name='data.xls', sheet_name='sheet1', data=[]):
    if len(data) == 0:
        print('Please input data')
        return
    wb = xlwt.Workbook(encoding='utf-8')
    my_sheet = wb.add_sheet(sheet_name)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    # font.bold = True
    # font.underline = True
    # font.italic = True
    style.font = font  # 设定样式
    data1 = data[0]
    fields = list(data1.keys())
    for i in range(len(fields)):
        my_sheet.write(0, i, fields[i])
    for i in range(len(data)):
        for j in range(len(fields)):
            my_sheet.write(i + 1, j, data[i][fields[j]])

    wb.save(excel_name)


"""
Writer a point to Excel
"""
def write_field_data(excel_name='data.xls', sheet_name='sheet1', x=0, y=0, data='data'):
    rb = xlrd.open_workbook(excel_name)
    wb = copy(rb)
    ws = wb.get_sheet(sheet_name)
    ws.write(x, y, data)
    wb.save(excel_name)