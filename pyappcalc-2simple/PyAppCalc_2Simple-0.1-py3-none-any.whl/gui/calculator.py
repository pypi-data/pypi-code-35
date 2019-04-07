# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calculator.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(436, 324)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.In_Frame = QtWidgets.QFrame(self.frame)
        self.In_Frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.In_Frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.In_Frame.setLineWidth(0)
        self.In_Frame.setObjectName("In_Frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.In_Frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.In_Num1 = QtWidgets.QLineEdit(self.In_Frame)
        self.In_Num1.setObjectName("In_Num1")
        self.horizontalLayout.addWidget(self.In_Num1)
        self.In_Num_2 = QtWidgets.QLineEdit(self.In_Frame)
        self.In_Num_2.setObjectName("In_Num_2")
        self.horizontalLayout.addWidget(self.In_Num_2)
        self.horizontalLayout_3.addWidget(self.In_Frame)
        self.In_Select_Op = QtWidgets.QComboBox(self.frame)
        self.In_Select_Op.setObjectName("In_Select_Op")
        self.In_Select_Op.addItem("")
        self.In_Select_Op.setItemText(0, "")
        self.In_Select_Op.addItem("")
        self.In_Select_Op.addItem("")
        self.In_Select_Op.addItem("")
        self.In_Select_Op.addItem("")
        self.In_Select_Op.addItem("")
        self.horizontalLayout_3.addWidget(self.In_Select_Op)
        self.Out_Result = QtWidgets.QLineEdit(self.frame)
        self.Out_Result.setObjectName("Out_Result")
        self.horizontalLayout_3.addWidget(self.Out_Result)
        self.Btn_Go = QtWidgets.QPushButton(self.frame)
        self.Btn_Go.setObjectName("Btn_Go")
        self.horizontalLayout_3.addWidget(self.Btn_Go)
        self.horizontalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 436, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.In_Select_Op.setItemText(1, _translate("MainWindow", "add"))
        self.In_Select_Op.setItemText(2, _translate("MainWindow", "sub"))
        self.In_Select_Op.setItemText(3, _translate("MainWindow", "div"))
        self.In_Select_Op.setItemText(4, _translate("MainWindow", "exp"))
        self.In_Select_Op.setItemText(5, _translate("MainWindow", "mul"))
        self.Btn_Go.setText(_translate("MainWindow", "Calc"))


