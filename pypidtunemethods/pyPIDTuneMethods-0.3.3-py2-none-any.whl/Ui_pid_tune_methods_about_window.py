# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\python\pyPIDTuneMethodsPlots\ui\Ui_pid_tune_methods_about_window.ui'
#
# Created: Thu Mar 26 15:51:05 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName(_fromUtf8("About"))
        About.resize(400, 80)
        About.setMinimumSize(QtCore.QSize(400, 80))
        About.setMaximumSize(QtCore.QSize(400, 80))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/info16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About.setWindowIcon(icon)
        About.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(About)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblVersion = QtGui.QLabel(About)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblVersion.setFont(font)
        self.lblVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.lblVersion.setObjectName(_fromUtf8("lblVersion"))
        self.verticalLayout.addWidget(self.lblVersion)
        self.lblURL = QtGui.QLabel(About)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblURL.setFont(font)
        self.lblURL.setAlignment(QtCore.Qt.AlignCenter)
        self.lblURL.setOpenExternalLinks(True)
        self.lblURL.setObjectName(_fromUtf8("lblURL"))
        self.verticalLayout.addWidget(self.lblURL)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        About.setWindowTitle(_translate("About", "About", None))
        self.lblVersion.setText(_translate("About", "pyPIDTuneMethods", None))
        self.lblURL.setText(_translate("About", "http://", None))

import PIDTuneMethods_rc
