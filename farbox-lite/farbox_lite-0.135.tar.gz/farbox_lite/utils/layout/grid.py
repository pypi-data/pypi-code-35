# coding: utf8
from __future__ import absolute_import



# 不支持自适应的逻辑

def re_key_for_layout_element(element, base=24):
    # 24 作为grid的基准，然后 0.33  1/4 等转为24为分母的值
    if not isinstance(element, dict) or not element.get('key'):
        return
    key = element.get('key')
    new_key = None
    if isinstance(key, (float, int)):
        if 0<key<=1: # 小数点
            new_key = int(round(base*key)) # 四舍五入的整数化
        elif key > base:
            new_key = base
    if new_key:
        element['key'] = new_key
    return ''



def re_key_for_layout_elements(elements, base=24):
    if isinstance(elements, (list, tuple)):
        for element in elements:
            re_key_for_layout_element(element, base)
    return ''



def split_elements_to_rows(elements, base=24):
    # 计算用于布局的 elements，这样最终在模板中渲染的时候，就直接调用属性就可以了
    rows = [[]]
    current_width = 0
    if not isinstance(elements, (list, tuple)):
        return rows

    re_key_for_layout_elements(elements, base=base)

    for element in elements:
        if not isinstance(element, dict):
            continue
        layout_key = element.get('key')

        if layout_key in ['h']: # 行 & 高度分割
            current_width = 0
            rows[-1].append(element)
            rows.append([])
            continue

        if isinstance(layout_key, (int, float)):
            new_current_width = current_width + int(layout_key)
            if new_current_width >= base: # 换行了
                current_width = 0
                rows[-1].append(element)
                rows.append([])
                continue
            else: # 还没有换行，当前总宽度增加
                current_width += int(layout_key)

        rows[-1].append(element)


    formatted_rows = [] # 有些元素属性，merge 到 row 上， 比如 bg
    property_fields = ['bg', 'style']
    for row in rows:
        if not row:
            continue
        formatted_row = dict()
        row_elements = []
        for element in row:
            key = element.get('key')
            if key in property_fields:
                formatted_row[key] = element
            else:
                if not key: # element 内的分行
                    if row_elements:
                        last_element = row_elements[-1]
                        last_element.setdefault('line_elements', []).append(element)
                else:
                    row_elements.append(element)

        formatted_row['elements'] = row_elements
        formatted_rows.append(formatted_row)


    return formatted_rows



