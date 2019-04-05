
"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import os

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
# ---------------------------------------------------------------------------------------------------------------------#


class VoltageDialog(qtWidgets.QDialog):

    def __init__(self, parent=None):
        super(VoltageDialog, self).__init__(parent)
        self.setWindowTitle("Generate Voltage")
        self.setFixedSize(230, 350)
        self.setFont(qtGui.QFont("Times", 10))

        self.voltage = []
        self.importedVoltage = True

        self.build_dialog()

    def build_dialog(self):
        dialogGridLyt = qtWidgets.QGridLayout()

        # --------------------------------------- Labels ----------------------------------------------#
        binsLbl = qtWidgets.QLabel("Bins")
        binsLbl.setAlignment(qtCore.Qt.AlignCenter)
        binsLbl.setFixedWidth(90)

        startLbl = qtWidgets.QLabel("Start Value")
        startLbl.setAlignment(qtCore.Qt.AlignCenter)
        startLbl.setFixedWidth(90)

        previewLbl = qtWidgets.QLabel("Voltage")
        previewLbl.setFont(qtGui.QFont("Times", 10, qtGui.QFont.Bold))

        self.gntVoltageNumLbl = qtWidgets.QLabel("")
        self.gntVoltageNumLbl.setFont(qtGui.QFont("Times", 10, qtGui.QFont.Bold))

        voltageLbl = qtWidgets.QLabel("Voltage")
        voltageLbl.setAlignment(qtCore.Qt.AlignCenter)
        voltageLbl.setFixedWidth(90)

        loopDirLbl = qtWidgets.QLabel("Direction")
        loopDirLbl.setAlignment(qtCore.Qt.AlignCenter)
        loopDirLbl.setFixedWidth(90)

        # ------------------------------------- Input -------------------------------------------#
        self.binsInpt = qtWidgets.QLineEdit()
        onlyDouble = qtGui.QDoubleValidator()
        self.binsInpt.setValidator(onlyDouble)

        self.startInpt = qtWidgets.QLineEdit()
        onlyDouble = qtGui.QDoubleValidator()
        self.startInpt.setValidator(onlyDouble)

        self.voltageInpt = qtWidgets.QLineEdit()
        onlyDouble = qtGui.QDoubleValidator()
        self.voltageInpt.setValidator(onlyDouble)

        self.voltagePreview = qtWidgets.QListWidget()
        self.voltagePreview.setFixedHeight(100)
        self.voltagePreview.setSelectionMode(qtWidgets.QAbstractItemView.NoSelection)

        self.loopDirection = qtWidgets.QComboBox()
        self.loopDirection.addItem("(+/-/-/+)")
        self.loopDirection.addItem("(+/+/-/-)")
        self.loopDirection.addItem("(-/-/+/+)")
        self.loopDirection.addItem("(-/+/-/+)")
        self.loopDirection.addItem("(+/-/+/-)")

        # --------------------------------------- Buttons ----------------------------------------------#
        importBtn = qtWidgets.QPushButton("Import")
        importBtn.setFixedWidth(80)
        importBtn.pressed.connect(self.importVoltage)

        cancelBtn = qtWidgets.QPushButton("Cancel")
        cancelBtn.setFixedWidth(80)
        cancelBtn.pressed.connect(self.close)

        generateBtn = qtWidgets.QPushButton("Generate")
        generateBtn.pressed.connect(self.generate_voltage)
        generateBtn.setFixedWidth(80)

        okayBtn = qtWidgets.QPushButton("Accept")
        okayBtn.pressed.connect(self.accept_voltage)
        okayBtn.setFixedWidth(80)

        # -----------------------------------Adding widgets to grid layout--------------------------------#
        dialogGridLyt.addWidget(startLbl, 0, 0)
        dialogGridLyt.addWidget(self.startInpt, 0, 1)
        dialogGridLyt.addWidget(voltageLbl, 1, 0)
        dialogGridLyt.addWidget(self.voltageInpt, 1, 1)
        dialogGridLyt.addWidget(binsLbl, 2, 0)
        dialogGridLyt.addWidget(self.binsInpt, 2, 1)
        dialogGridLyt.addWidget(loopDirLbl, 3, 0)
        dialogGridLyt.addWidget(self.loopDirection, 3, 1)
        dialogGridLyt.addWidget(importBtn, 4, 0)
        dialogGridLyt.addWidget(generateBtn, 4, 1, alignment=qtCore.Qt.AlignRight)
        dialogGridLyt.addWidget(previewLbl, 5, 0)
        dialogGridLyt.addWidget(self.gntVoltageNumLbl, 5, 1)
        dialogGridLyt.addWidget(self.voltagePreview, 6, 0, 2, 2)
        dialogGridLyt.addWidget(cancelBtn, 9, 0)
        dialogGridLyt.addWidget(okayBtn, 9, 1, alignment=qtCore.Qt.AlignRight)

        self.setLayout(dialogGridLyt)

    def show_dialog(self):
        self.voltage = []
        self.exec_()

    def generate_voltage(self):
        if self.dialogError() is False:
            self.gntVoltageNumLbl.setText("")
            self.voltagePreview.clear()

            voltage = []
            startVal = float(self.startInpt.text())
            appliedVoltage = float(self.voltageInpt.text())
            bins = float(self.binsInpt.text())
            direction = self.loopDirection.currentText().replace("(", "").replace(")", "").split("/")

            rate = (appliedVoltage/2)/(bins/4)
            loopMax = bins/4
            loopMax = int(loopMax)
            val = startVal
            for d in direction:
                if d == "+":
                    voltage.append(val)
                    self.voltagePreview.addItem(str(val))
                    for i in range(loopMax-1):
                        val = val + rate
                        voltage.append(val)
                        self.voltagePreview.addItem(str(val))
                elif d == "-":
                    voltage.append(val)
                    self.voltagePreview.addItem(str(val))
                    for i in range(loopMax-1):
                        val = val - rate
                        voltage.append(val)
                        self.voltagePreview.addItem(str(val))
            self.gntVoltageNumLbl.setText(str(len(voltage)))
            self.voltage = voltage

    def importVoltage(self):
        try:
            self.gntVoltageNumLbl.setText("")
            self.voltagePreview.clear()
            voltage = []
            selectedFilter = "Text files (*.txt)"
            file, fileFilter = qtWidgets.QFileDialog.getOpenFileName(self, "Open Voltage File", "", selectedFilter)
            inputFile = open(file, "r")
            lines = inputFile.readlines()
            for line in lines:
                line.strip("\n")
                for v in line.split(","):
                    if v.strip() != "":
                        voltage.append(v)
                        self.voltagePreview.addItem(v)
            self.voltage = voltage
            self.gntVoltageNumLbl.setText(str(len(voltage)))
        except Exception as ex:
            qtWidgets.QMessageBox.warning(self, "Error", "There was an error opening the file. Please make sure"
                                                         "it follows the proper format.\n Each value should be "
                                                         "separated by a comma.\nExp: \n2.0,\n2.1")

    def dialogError(self):
        error = False
        startVal = self.startInpt.text()
        appliedVoltage = self.voltageInpt.text()
        bins = self.binsInpt.text()

        if startVal == "" or appliedVoltage == "" or bins == "":
            error = True

        return error

    def accept_voltage(self):
        if self.voltage:
            self.importedVoltage = True
            self.close()








