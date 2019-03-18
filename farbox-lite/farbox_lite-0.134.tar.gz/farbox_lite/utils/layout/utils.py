# coding: utf8
from __future__ import absolute_import
from farbox_lite.utils.lazy import to_int, to_float
import re


special_grid_factors = {
    0.2: '1/5',
    0.4: '2/5',
    0.6: '3/5',
    0.8: '4/5',
}
def get_grid_factor(k, base=24, odd_base=5):
    # 一般有两套，比如 1/5 就对应不到 24 中
    k = special_grid_factors.get(k) or k

    if not k:
        return k, base

    if isinstance(k, (str,unicode)):
        if '-' in k or '/' in k:
            v1, v2 = re.split(r'-|/', k, maxsplit=1)
            v1 = to_int(v1)
            v2 = to_int(v2)
            if v1 and v2:
                small_one = min(v1, v2)
                big_one = max(v1, v2)
                if big_one == odd_base:
                    base = odd_base
                k = float(small_one)/float(big_one)
        elif '.' in k:
            k = to_float(k)
        else: # 整数
            k = to_int(k) or 1

    if k and isinstance(k, int) and k>1:
        k = float(k)/base

    if isinstance(k, (float, int)) and k<=1:
        # 之前全部处理为分数了, 这样 1 就是全值了
        k *= base

    # 处理最终的 k 值
    k = to_int(round(k)) or base # 四舍五入并 int
    if k > base:
        k = base
    if k < 1:
        k = 1
    return k, base




def test_get_grid_factor():
    print get_grid_factor(0)
    print get_grid_factor(0.001)
    print get_grid_factor(1)
    print get_grid_factor(0.1)
    print get_grid_factor('0.1')
    print get_grid_factor(0.3)
    print get_grid_factor(0.33)
    print get_grid_factor('1/3')
    print get_grid_factor('1/5')
    print get_grid_factor('1-5')
    print get_grid_factor('2-5')
    print get_grid_factor('5-5')
    print get_grid_factor('2-3')
    print get_grid_factor('2、3') # 会被当做整个单位，因为无法识别
    print get_grid_factor('2/3')


if __name__ == '__main__':
    test_get_grid_factor()