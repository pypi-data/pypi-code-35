def get_dict_name(xpath):
    return xpath.split('/')[-1]


def get_float_value(xpath, doc):
    return float(doc.xpath(xpath)[0].text)



