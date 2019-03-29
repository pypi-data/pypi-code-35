"""
将文件相关的常用方法聚集在这里
"""
import os, os.path as path, codecs, chardet, shutil, copy


def touch(file):
    """
    追加模式打开文件并更新Mtime,文件不存在新建
    :param file:
    :return:
    """
    with open(file, 'a'):
        os.utime(file, None)


def rename(src, dest):
    """
    os.rename(src, dest)
    :param src:
    :param dest:
    :return:
    """
    os.rename(src, dest)


def copy(src, dest):
    """
     shutil.copyfile(src,dest)
    :param src:
    :param dest:
    :return:
    """
    shutil.copyfile(src, dest)


def move(src, dest):
    """
    shutil.move(src, dest)
    :param src:
    :param dest:
    :return:
    """
    return shutil.move(src, dest)


def remove(file):
    """
    删除文件 os.remove
    :param file:
    :return None:
    """
    assert exist(file), "文件不存在"

    os.remove(file)


def exist(file):
    """
    path.exists
    :param file:
    :return:
    """
    return path.exists(file)


def is_file(file):
    """
    os.path.isfile(file)
    :param file:
    :return:
    """
    return path.isfile(file)


def is_abs(file):
    """
    os.path.isabs(file)
    :param file:
    :return:
    """
    return path.isabs(file)


def dirname(file):
    """
    os.path.dirname(file)
    :param file:
    :return:
    """
    return os.path.dirname(file)


def basename(file):
    """
    os.path.basename(file)
    :param file:
    :return:
    """
    return os.path.basename(file)


def line_separator():
    """
    os.linesep
    :return:
    """
    return os.linesep


def size(file):
    """
    os.path.getsize(file)
    :param file:
    :return:
    """
    return path.getsize(file)


def lines(file, mode='r', strip_str=None, encoding="utf-8"):
    """
    读取文件中的所有行并返回
    :param str file: 文件路径
    :param str mode:   读取文件模式
    :param str strip_str: 行清空字符串
    :param str  encoding: 读取文件的编码方式
    :return:
    """

    assert exist(file), "文件不存在"

    lines = []
    with open(file, mode=mode, encoding=encoding) as f:
        for line in f:
            # 是否按照特殊的字符来清空行
            if strip_str is None:
                lines.append(line.strip())
            else:
                lines.append(line.strip(strip_str))

    return lines


def trancate(file):
    """
    清空文件内容
     f.seek(0)
     f.truncate()
    :param file:
    :return:
    """
    with open(file, mode="r+") as f:
        f.seek(0)
        f.truncate()


def has_bom(file):
    """
     检测文件是否包含utf8-bom
    :param file:
    :return Bool: true if has,else false
    """
    with open(file, "rb+") as file:
        file_contents = file.read()
        if file_contents[:3] == codecs.BOM_UTF8:
            return True
        else:
            return False


def clean_bom(file):
    """
    清理文件的bom
    :param file:
    :return :
    """
    if has_bom(file):
        with open(file, "rb+") as f:
            file_contents = f.read()
            f.seek(0)
            f.truncate()
            f.write(file_contents[3:])


def is_utf8(file):
    """
    检测文件是否utf-8编码的
    :param file:
    :return Bool :true if utf-8 encoding
    """
    with open(file, "rb+") as f:
        file_contents = f.read()
        char_det_detect = chardet.detect(file_contents)
        if char_det_detect['encoding'] in ["utf-8", "ascii"]:
            return True

    return False


def convert2utf8(file):
    """
    把文件转成 utf-8 编码
    :param file:
    :return:
    """
    if not is_utf8(file):
        return

    with open(file, "rb+") as f:
        file_contents = f.read()

        char_det_detect = chardet.detect(file_contents)
        new_con = file_contents.decode(char_det_detect['encoding'])

        f.seek(0)
        f.truncate()

        f.write(new_con.encode("utf-8"))


def extension(file):
    """
    os.path.splitext(file)
    :param file:
    :return:
    """
    return path.splitext(file)


def compare_lines(file_a, file_b):
    """
    比较两个文件的行 返回一个含有 not_b,not_a,a_and_b 三个key的字典,值对应着结果行列表
    :param str file_a:
    :param str file_b:
    :return :
    """
    lines_a = lines(file_a)
    lines_b = lines(file_b)

    return {
        "not_a": [line for line in lines_b if line not in lines_a],
        "not_b": [line for line in lines_a if line not in lines_b],
        "a_and_b": copy.deepcopy(lines_a).extend(lines_b)
    }
