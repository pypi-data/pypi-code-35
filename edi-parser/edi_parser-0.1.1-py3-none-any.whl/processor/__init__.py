from typing import Union, List


def normalize(data: Union[int, str]) -> str:
    data = str(data).replace(':', '').replace('.', '').replace('-', '').replace('/', '').replace(',', '')
    return data


def parse_header_trailer(value: list, template: dict, type_rules: dict) -> str:
    final_value = ''
    item_info = template[value[0]]
    for i, item in enumerate(value):
        item_size = item_info[i]['size']
        item_type = item_info[i]['type']

        if type_rules[item_type]['normalize'] and ('normalize' not in item_info[i] or item_info[i]['normalize']):
            item = normalize(item)

        if len(item) == item_size:
            final_value += item
        elif len(item) > item_size:
            final_value += item[:item_size]
        else:
            add_str = ''
            for x in range(item_size - len(item)):
                add_str += type_rules[item_type]['character']
            if type_rules[item_type]['place'] == 'start':
                final_value += add_str + item
            elif type_rules[item_type]['place'] == 'end':
                final_value += item + add_str
    return final_value


def parse_content(value: list, template: dict, type_rules: dict) -> str:
    final_value = ''
    item_info = template[value[0]]
    for i, item in enumerate(value):
        item_size = item_info[i]['size']
        item_type = item_info[i]['type']

        if type_rules[item_type]['normalize'] and ('normalize' not in item_info[i] or item_info[i]['normalize']):
            item = normalize(item)

        if len(item) == item_size:
            final_value += item
        elif len(item) > item_size:
            final_value += item[:item_size]
        else:
            add_str = ''
            for x in range(item_size - len(item)):
                add_str += type_rules[item_type]['character']
            if type_rules[item_type]['place'] == 'start':
                final_value += add_str + item
            elif type_rules[item_type]['place'] == 'end':
                final_value += item + add_str
    return final_value


def parse(template: dict, type_rules: dict, order_rules: list,
          data: List[List[Union[str, int]]]) -> list:
    headers = data[0:order_rules.index('*')]
    contents = data[order_rules.index('*'):len(data) - len(order_rules[order_rules.index('*') + 1])]
    trailers = data[len(data) - len(order_rules[order_rules.index('*') + 1:]):]

    final_data = []
    for index, item in enumerate(headers):
        final_data.append(parse_header_trailer(item, template, type_rules))

    for index, item in enumerate(contents):
        final_data.append(parse_content(item, template, type_rules))

    for index, item in enumerate(trailers):
        final_data.append(parse_header_trailer(item, template, type_rules))
    return final_data
