"""
使用python3.7编写一些自己常用的python包
create by swm 20181120
"""


def hello_swm():
    print("Hi, I am october, thanks for using this packages!")


def the_system() -> str:
    """
    当前操作系统
    :return:
    """
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'OSX'
    elif platform == "win32":
        return 'windows'


def get_all_indices(element, alist):
    """
    Find the index of an element in a list. The element can appear multiple times.
    input:  alist - a list
            element - objective element
    output: index of the element in the list
    """
    result = []
    offset = -1
    while True:
        try:
            offset = alist.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)


def find_highest_values(l: list, num=3) -> list:
    """
    查找一个列表中评率最高的值，默认为前三个
    :param l:
    :param num:
    :return:
    """
    from collections import Counter
    cnt = Counter(l)
    return cnt.most_common(num)


def check_letters(str1, str2) -> bool:
    """
    检查两个字符串是否由相同字母的不同顺序组成
    :param str1:
    :param str2:
    :return:
    """
    from collections import Counter
    resbool = Counter(str1) == Counter(str2)
    return resbool


def min_index(lst: list) -> int:
    """
    列表中最小值的索引
    :param l:
    :return:
    """
    return min(range(len(lst)), key=lst.__getitem__)


def max_index(lst: list) -> int:
    """
    列表中最大值的索引
    :param lst:
    :return:
    """
    return max(range(len(lst)), key=lst.__getitem__)


def remove_duplicate_elements(lst: list) -> list:
    """
    移除一个列表中重复的元素
    对列表中出现的元素进行去重
    数据类似于：
    items = ["foo", "bar", "bar", "foo"]
    :param lst: 
    :return: 
    """
    from collections import OrderedDict
    # items = ["foo", "bar", "bar", "foo"]
    return list(OrderedDict.fromkeys(lst).keys())


def unicodestr_to_string(ustring: str) -> str:
    """
    unicode 的字符串，解码成中文
    :param ustring:'\u5546\u8baf\u4fe1\u606f'
    :return:
    """
    # data = ustring.encode('latin-1').decode('unicode_escape')
    return repr(ustring)


def sorteddict(d: dict):
    """
    对dict中的数据进行排序
    条件：value为int数字
    类似于：
    d = {'apple': 10, 'orange': 20, 'banana': 5, 'tomatto': 1}
    :param d:
    :return:
    """
    res = sorted(d.items(), key=lambda x: x[1])
    return res



if __name__ == '__main__':
    d = '\u5546\u8baf\u4fe1\u606f'
    # c = unicodestr_to_string(d)
    print(repr(d))
