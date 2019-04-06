# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bkd/pyqt/kdui2py/kdui2py/kdui2py.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(402, 272)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_convert_single_file = QtWidgets.QPushButton(Form)
        self.pb_convert_single_file.setObjectName("pb_convert_single_file")
        self.gridLayout.addWidget(self.pb_convert_single_file, 1, 0, 1, 1)
        self.pb_single_dir = QtWidgets.QPushButton(Form)
        self.pb_single_dir.setObjectName("pb_single_dir")
        self.gridLayout.addWidget(self.pb_single_dir, 1, 2, 1, 1)
        self.pb_dir_and_subdir = QtWidgets.QPushButton(Form)
        self.pb_dir_and_subdir.setObjectName("pb_dir_and_subdir")
        self.gridLayout.addWidget(self.pb_dir_and_subdir, 1, 3, 1, 1)
        self.tb_result = QtWidgets.QTextBrowser(Form)
        self.tb_result.setObjectName("tb_result")
        self.gridLayout.addWidget(self.tb_result, 2, 0, 1, 4)
        self.pb_preview = QtWidgets.QPushButton(Form)
        self.pb_preview.setObjectName("pb_preview")
        self.gridLayout.addWidget(self.pb_preview, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.le_suffix = QtWidgets.QLineEdit(Form)
        self.le_suffix.setObjectName("le_suffix")
        self.gridLayout.addWidget(self.le_suffix, 0, 1, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "kdui2py"))
        self.pb_convert_single_file.setText(_translate("Form", "单个文件"))
        self.pb_single_dir.setText(_translate("Form", "单个目录"))
        self.pb_dir_and_subdir.setText(_translate("Form", "目录及其子目录"))
        self.pb_preview.setText(_translate("Form", "预览UI文件"))
        self.label.setText(_translate("Form", "文件名后缀："))
        self.le_suffix.setText(_translate("Form", "_ui"))

