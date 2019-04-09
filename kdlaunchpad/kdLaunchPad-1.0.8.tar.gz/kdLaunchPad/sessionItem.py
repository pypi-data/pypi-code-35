'''
Created on 2019年3月22日

@author: bkd
'''

import os

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QFileDialog

class sessionItem(QDialog):
    def __init__(self,last_path = None):
        super().__init__()
        loadUi("sessionItem.ui", self)
        self.last_path = last_path
    
    @pyqtSlot()
    def on_pb_open_file_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                    "閫夋嫨鏂囦欢",
                                     self.last_path,
                                    "All Files (*)")   #璁剧疆鏂囦欢鎵╁睍鍚嶈繃婊�,娉ㄦ剰鐢ㄥ弻鍒嗗彿闂撮殧
        if filename:
            print(filename)
            self.le_cmd.setText(filename)
            self.le_name.setText(os.path.basename(filename))
