#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
from datetime import datetime


def get_data_with_id(data):
    # Transforms the data into a dictionary with the variable's id and the corresponding data for that variable
    var = {}
    for i in data:
        var[i['id'].split('/d')[1]] = i['data']
    return var


def data_to_dataframe(datas, datadefs, ref):
    # Return a dataframe based on the given data
    data = get_data_with_id(datas)
    index = []
    result = {}
    for i in datadefs:
        if str(i['id']) in data.keys():
            if str(i['id']) == ref['referenceDate'].split('/d')[1]:
                for j in data[str(i['id'])]:  # Changes the format of the date to be readable
                    data[str(i['id'])][data[str(i['id'])].index(j)] = datetime.strptime(j, "%Y%m%d_%H%M%S") \
                        .strftime("%Y/%m/%d_%H:%M:%S")
                index = data[str(i['id'])]
            else:
                result[i['local']] = data[str(i['id'])]
    dataframe = pd.DataFrame(result, index=index)
    print("Your data has been recovered")
    return dataframe
