# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/azzamsya/rhd/azzamsa/self-management/references/masterpiece/software/code/projects/lup/lupr/lupr/views/interval_prompt.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(281, 82)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.interval_spin = QtWidgets.QSpinBox(Dialog)
        self.interval_spin.setMaximum(10000)
        self.interval_spin.setObjectName("interval_spin")
        self.verticalLayout.addWidget(self.interval_spin)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.apply_btn = QtWidgets.QPushButton(Dialog)
        self.apply_btn.setObjectName("apply_btn")
        self.horizontalLayout.addWidget(self.apply_btn)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set Interval"))
        self.apply_btn.setText(_translate("Dialog", "apply"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))

