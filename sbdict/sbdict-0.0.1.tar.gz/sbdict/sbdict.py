#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author:  sennhvi
# @Email:   sennhvi@gmail.com
# @Date:    3/20/19

import requests
import json

query_url = "https://fanyi.youdao.com/translate"
params = {"doctype": "json"}

word = input(">")
while ( word != "exit"):
    params["i"] = word
    try:
        response = requests.get(query_url, params=params)
        print(json.loads(response.text)["translateResult"][0][0]["tgt"])
    except Exception as e:
        print("Error: %s" %str(e))
    word = input(">")
