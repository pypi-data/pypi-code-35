# coding: utf-8

import os
import sys
import uuid
import hashlib
import time
import requests
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from . import from_to_type
from .fileutil import get_file_realpath,check_and_create


class kdYoudaoDictionary(QWidget):
    def __init__(self):
        super(kdYoudaoDictionary, self).__init__()
        loadUi(get_file_realpath("kdYoudaoDictionary.ui"), self)
        self.setWindowIcon(QIcon(get_file_realpath('data/Dictionary-icon.png')))
        

        for translate_type in from_to_type.translate_types:
            self.cb_from_to.addItem(translate_type[1])

        appKey_config_file = get_file_realpath("appKey_config.json")
        check_and_create(appKey_config_file)
        with open(appKey_config_file, "r",encoding="utf-8") as f:
            content = f.read().strip()
            if content != "":
                conf = json.loads(content)
                self.appKey = conf["appKey"]
                self.secret_key = conf["secret_key"]

    def on_pb_translate_clicked(self):
        if self.chkB_detail.isChecked():
            self._translate_detail()
        else:
            self._translate()

    def on_le_word_returnPressed(self):
        if self.chkB_detail.isChecked():
            self._translate_detail()
        else:
            self._translate()

    # ～ 免费的调用模式
    def _translate(self):
        word = self.le_word.text().strip()
        if word == "":
            pass
        else:
            cur_type = self.cb_from_to.currentText()
            for translate_type in from_to_type.translate_types:
                if translate_type[1] == cur_type:
                    url = "http://fanyi.youdao.com/translate?&doctype=json&type={}&i={}".format(
                        translate_type, word)
                    r = requests.get(url)
                    print("结果：",r.text)
                    result = json.loads(r.text)
                    if result["errorCode"] == 0:
                        self.tb_result.setText(
                            result["translateResult"][0][0]["tgt"])
    # ～ 调用个人的API key来查询，收费

    def _translate_detail(self):
        word = self.le_word.text().strip()
        if word == "":
            pass

        salt = str(uuid.uuid1())
        now = str(int(time.time()))
        input_word = None
        if len(word) > 20:
            input_word = word[:10] + str(len(word))+word[11:]
        else:
            input_word = word

        params = {}
        cur_type = self.cb_from_to.currentText()
        for translate_type in from_to_type.translate_types:
            if translate_type[1] == cur_type:
                origin_type = translate_type[0].replace("ZH_CN","zh-CHS").replace("KR","ko")
                types = origin_type.split("2")
                params["from"] = types[0].lower()
                params["to"] = types[1].lower()

        params["q"] = word
        params["appKey"] = self.appKey
        params["salt"] = salt
        sign_source = str(self.appKey + input_word + salt + now + self.secret_key).encode()
        params["sign"]=str(hashlib.sha256(sign_source).hexdigest())
        params["signType"] = "v3"
        params["curtime"] = now
        print("入參:",params)
        r = requests.get(
            "https://openapi.youdao.com/api", params=params)
        result = json.loads(r.text)
        print("结果："+r.text)

        if result["errorCode"] != "0":
            pass
        show_result = result["translation"][0]
        if "web" in result.keys():
            show_result += "\n网络释义:\n"
            web = result["web"]
            for w in web:
                show_result = show_result + "    " + \
                    w["key"] + "," + ",".join(w["value"]) + "\n"
        self.tb_result.setText(show_result)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = kdYoudaoDictionary()
    win.show()
    sys.exit(app.exec_())
