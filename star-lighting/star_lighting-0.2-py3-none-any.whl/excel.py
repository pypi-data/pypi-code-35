import os
import numpy
import xlrd
import xlwt


class Excel:
    def __init__(self, file=None, index=0):
        if file:
            if not os.path.isfile(file):
                raise FileNotFoundError('文件{}不存在'.format(file))
            else:
                self.load(file, index)
        self.workbook = None
        self.sheets = None
        self.sheet = None
        self.rowNum = 0
        self.colNum = 0
        self.data = list()

    def load(self, file: str, index=0):
        """'
        file:   str, 表示要加载的文件
        index： (int,str), 表示要加载的sheet
        """
        self.workbook = xlrd.open_workbook(file)
        self.sheets = self.workbook.sheets()
        if isinstance(index, int):
            if index < len(self.sheets):
                self.sheet = self.workbook.sheets()[index]
            else:
                raise IndexError(f'输入的页码{index}不存在')
        elif isinstance(index, str):
            self.workbook.sheet_by_name(index)
        else:
            raise TypeError(f'{index}参数错误～')
        print(f'正在加载文件{file}...')
        self.rowNum = self.sheet.nrows  # sheet行数
        self.colNum = self.sheet.ncols  # sheet列数

        # 获取所有单元格的内容
        _list = []
        for i in range(self.rowNum):  # 第0行到 rowNum-1 行
            rowlist = []
            for j in range(self.colNum):  # 第0列到 rowNum-1 列
                rowlist.append(self.sheet.cell_value(i, j))
            _list.append(rowlist)
        self.data = _list
        print(f'文件{file}加载完毕～')

    def make(self, data, fimename='name1.xls', sheetname='sheet1'):
        """生成一个excel文件"""
        if not fimename.endswith('.xls'):
            raise TypeError(f'fimename 参数必须以.xls结尾')

        f = xlwt.Workbook()
        sheet1 = f.add_sheet(sheetname=sheetname, cell_overwrite_ok=True)
        if isinstance(data, numpy.ndarray):
            if data.ndim == 1:
                rows = 1
                colums = data.shape[0]  # 列数
            elif data.ndim == 2:  # 深度大于等于2
                rows = data.shape[0]
                colums = data.shape[1]  # 列数
            elif data.ndim > 2:
                rows = data.shape[0]
                colums = data.shape[1]  # 列数
                print(f'警告：{data}的维度大于2维, 深度大于2层的数据将舍弃～')
            else:
                raise TypeError(f'文件{data}格式（维度）错误～')
            for i in range(rows):
                for j in range(colums):
                    sheet1.write(i, j, f'{data[i][j]}')
        elif isinstance(data, (list, tuple)):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    sheet1.write(i, j, f'{data[i][j]}')
        else:
            raise TypeError(f'文件{data}类型错误')
        f.save(fimename)

    def print(self, part='all', n=100):
        """
        打印出来
        :return:
        """
        # 输出所有单元格的内容
        print('行：', self.rowNum, '列：', self.colNum)
        if part == 'all':
            for i in range(self.rowNum):
                for j in range(self.colNum):
                    print(self.data[i][j], '\t\t', end="")
                print()
        elif part == 'head':
            n = 0 if n - 1 <= 0 else self.rowNum if n - 1 >= self.rowNum else n
            for i in range(n):
                for j in range(self.colNum):
                    print(self.data[i][j], '\t\t', end="")
                print()
        elif part == 'tail':
            n = 0 if n - 1 <= 0 else self.rowNum if n - 1 >= self.rowNum else n
            for i in range(n - 1, self.rowNum):
                for j in range(self.colNum):
                    print(self.data[i][j], '\t\t', end="")
                print()
        else:
            raise ValueError(f'part参数{part}错误')



