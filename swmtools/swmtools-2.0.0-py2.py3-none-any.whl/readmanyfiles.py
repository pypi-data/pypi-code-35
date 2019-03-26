"""
读取各种不同文件的方法
create by swm 2019/03/25
"""
import csv
from pathlib import Path
import xml.dom.minidom as xml
import xlrd


def readcsvfile(csvname, skipheader=True):
    """
    是否跳过第一行
    读取一个csv文件的所有行数，返回一个迭代器
    :param csvname:
    :return:
    """
    with open(csvname, newline='', encoding='utf-8') as csvfile:
        dialect = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        if dialect:
            next(csvfile)
        reader = csv.reader(csvfile)
        # 跳过标题
        if skipheader:
            next(reader)
        for row in reader:
            yield row


def read_xlsx_file(xlsxfilename, skipheader=True):
    """
    读取xlsx文件，返回一个迭代器
    skipheader表示为是否跳过首行
    :param xlsxfilename:
    :param skipheader:
    :return:
    """
    workbook = xlrd.open_workbook(xlsxfilename)
    worksheet = workbook.sheet_by_index(0)
    start_index = 0
    if skipheader:
        start_index += 1
    for row in range(1, worksheet.nrows):
        line = worksheet.row_values(row)
        yield line


def read_xml_file(xmlfilename, decode='utf-8'):
    """
    读取xmlfile文件，并指定文件的解码方式，默认为utf-8
    返回dom树
    :param xmlfilename:
    :param decode:
    :return:
    """
    if isinstance(xmlfilename, Path):
        xmlfile: Path = xmlfilename
    else:
        xmlfile = Path(xmlfilename)
    with xmlfile.open('rb') as xf:
        lines = xf.read()
        res_lines = bytes.decode(lines, decode)
        dom = xml.parseString(res_lines)
    return dom


def save_data_as_csv(csvname: str, header: list, lines: list):
    """
    将数据保存到csv文件
    默认传入文件名
    :param csvname:
    :param header:[属性1， 属性2， 属性3]
    :param lines: [{属性1：值1}，{属性2：值2}， {属性3：值3}]
    :return:
    """
    csvfile = open(csvname, 'a', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for write_line in lines:
        writer.writerow(write_line)
    csvfile.close()


if __name__ == '__main__':
    read_xlsx_file(r'D:\swmdata\spiderdonwloadbak\data\20190320-4ce5b849fb9473f5.xlsx')
    # res = read_xml_file(r"D:\xunlei\Profiles\Community\CooperatorImages\unionInfo_new.xml")
    # print(res)
