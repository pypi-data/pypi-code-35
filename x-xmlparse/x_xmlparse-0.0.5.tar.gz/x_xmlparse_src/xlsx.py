import xlrd
import  os
from .core import  ParseSlice
import  json


def parse(contents,parse,  *columns, name='',context=False, tp=''):
    if isinstance(contents, str) and os.path.exists(contents):
        workbook = xlrd.open_workbook(contents)
    else:
        assert isinstance(contents , bytes) is True
        workbook = xlrd.open_workbook(file_contents=contents, encoding_override='cp1252')

    

    names = workbook.sheet_names()
    if tp == 'info':
        for n in names:
            _sheet = workbook.sheet_by_name(n)
            _first_row = [] # The row where we stock the name of the column
            for col in range(_sheet.ncols):
                _first_row.append( _sheet.cell_value(0,col) )

            print("[%s]" % n, *_first_row)
        return 

    if not name:
        name = names[0]
    sheet = workbook.sheet_by_name(name)
    


    if parse:
        parse, _slice = ParseSlice(parse)
        et = _slice.stop  if _slice.stop  is not None else   sheet.nrows
        st = _slice.start  if _slice.start  is not None  else 0
        _slice = slice(st, et)
    else:
        _slice = slice(0, sheet.nrows)

    


    first_row = [] # The row where we stock the name of the column
    for col in range(sheet.ncols):
        first_row.append( sheet.cell_value(0,col) )
    # tronsform the workbook to a list of dictionnary
    

    data =[]
    nrows_e = min([_slice.stop, sheet.nrows])
    nrows_s = max([_slice.start, 1])
    if tp !='json':
        print(','.join([str(i) for i in first_row]))

    for row in range(nrows_s, nrows_e):
        elm = {}
        found = False
        for col in range(sheet.ncols):
            if columns:
                if col in columns:
                    elm[first_row[col]]=sheet.cell_value(row,col)
            else:
                elm[first_row[col]]=sheet.cell_value(row,col)
            if parse.strip():
                if parse.strip() in str(sheet.cell_value(row,col)):
                    found = True
            else:
                found = True

        if found:
            if tp == 'json':
                print(json.dumps(elm))
            else:
                print(','.join([str(i) for i in elm.values()]))