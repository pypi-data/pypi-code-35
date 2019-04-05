#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

#C In some methods LFit or L refer to the Lattice Constant not RLU
"""

# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import os

import PyQt5.QtWidgets as qtWidgets
import numpy as np

from xPlotUtil.Source.GaussianFit import GaussianFitting
import traceback


# ---------------------------------------------------------------------------------------------------------------------#


class ReadSpec:
    """Loads spec file and gets appropriate information from it for a certain PVvalue/scan
    """

    def __init__ (self, parent=None):
        self.dockedOpt = parent
        self.myMainWindow = self.dockedOpt.myMainWindow
        self.gausFit = GaussianFitting(self)
        self.lorentFit = self.gausFit.lorentFit
        self.algebraExp = self.gausFit.algebraExp
        self.specFileOpened = False
        self.specFileName = None

        # Initializing lattice information
        self.lElement = 0
        self.lMax = 0
        self.lMin = 0

    def openSpecFile(self):
        """This method calls on the file dialog to open the spec file if no previous spec file has been open. Otherwise
        it asks the user if he wants to open a new spec file.
        """
        if self.specFileOpened == False:
            self.openSpecDialog()
        elif self.specFileOpened == True:
            response = self.dockedOpt.msgApp("Open New Spec File", "Would you like to open a new spec file?")
            if response == "Y":
                self.openSpecDialog()

    def getPVNumKey(self, text):
        h = text.split('.')
        return int(h[1])

    def openSpecDialog(self):
        """This method creates a file dialog to open the spec file. Once the file has been open it resets
        various attributes to their original value to initialize/reestablish functionality.
        """
        try:
            selectedFilter = "Spec files (*.spec)"
            self.specFileName, self.specFileFilter = qtWidgets.QFileDialog.getOpenFileName(self.myMainWindow, "Open Spec File",
                                                                                 None, selectedFilter)
            # Makes sure a file has been opened
            if os.path.isfile(self.specFileName):
                # Gets the PVvalue files in the directory
                self.specDirectory = os.path.dirname(self.specFileName)
                self.PvFiles = [f for f in os.listdir(self.specDirectory) if f.find("PVvalue") == 0]
                self.PvFiles.sort(key=self.getPVNumKey)

                self.dockedOpt.mainOptions.close()
                self.dockedOpt.DockMainOptions()
                self.dockedOpt.fitStat = False
                self.dockedOpt.LFitStat = False
                self.dockedOpt.normalizingStat = False
                self.algebraicExpStat = False
                self.dockedOpt.specFileInfo()
                self.specFileOpened = True
                self.dockedOpt.fileOpened = False
                self.continueGraphingEachFit = True
                self.myMainWindow.latticeFitAction.setEnabled(False)
                self.myMainWindow.showProgress("Spec file opened")
        except Exception as e:
            qtWidgets.QMessageBox.warning(self.myMainWindow, "Error", "There was an error \n\n Exception: " + str(e)
                                + "\n\nTraceback: " + str(traceback.print_stack()))

    def loadScans(self, scans):
        """Loads the scan into the specDataList
        :param scans: list of scans provided using spec2nexus.spec
        """
        self.scans = scans
        scanKeys = self.scans.keys()
        sorted(scanKeys, key=int)  # Sorts the scans in order lowest-greater
        for scan in scanKeys:
            for file in self.PvFiles:
                f = file.split('.')
                if f[1] == scan:
                    PValue = 'PVvalue #' + str(scans[scan].scanNum)
                    self.dockedOpt.specDataList.addItem(PValue)

    def currentScan(self):
        """This method calls on the open file dialog to open the PVvalue file. It gets the required data
        from the  spec file for the PVvalue/scan.
        """
        scan = self.PvFiles[self.dockedOpt.specDataList.currentRow()].split(".")
        self.scan = scan[1]
        self.currentRow = self.dockedOpt.specDataList.currentRow()

        if self.specDirectory.find("/") != -1:
            fileName = self.specDirectory + "/" + self.PvFiles[self.currentRow]
        else:
            fileName = self.specDirectory + "\\" + self.PvFiles[self.currentRow]

        self.dockedOpt.openFile(fileName)

        # Making sure the file of the PVvalue has been opened
        if self.dockedOpt.fileOpened == True:
            try:
                if os.path.isfile(self.dockedOpt.fileName):
                    self.normalizers = [] # Array that will contain possible normalizers
                    self.L = []  # Array of the RLU

                    self.L = self.scans[self.scan].data["L"]
                    self.lMin = self.L[0]
                    self.lMax = self.L[-1]

                    k = self.scans[self.scan].G["G1"].split(" ")
                    self.lElement = float(k[2])

                    # Gets possible normalizer values
                    for key in self.scans[self.scan].data.keys():
                        if key.find("Ion_Ch_") == 0:
                            self.normalizers.append(key)
                    sorted(self.normalizers)
            except Exception as e:
                qtWidgets.QMessageBox.warning(self.myMainWindow, "Error", "There was an error \n\n Exception: " + str(e))


    def NormalizerDialog(self):
        """This method creates a dialog with dynamically created radio buttons from the spec file, which allow the
        user to pick which chamber was used to normalize.
        """
        if self.dockedOpt.normalizingStat == False and self.dockedOpt.FileError() == False :
            self.normalizeDialog = qtWidgets.QDialog(self.myMainWindow)
            dialogBox = qtWidgets.QVBoxLayout()
            buttonLayout = qtWidgets.QHBoxLayout()
            vBox =qtWidgets.QVBoxLayout()

            groupBox = qtWidgets.QGroupBox("Select normalizer")
            self.buttonGroup = qtWidgets.QButtonGroup(groupBox)

            for norm in self.normalizers:
                normalizerRB = qtWidgets.QRadioButton(norm)
                self.buttonGroup.addButton(normalizerRB, int(norm[-1]))
                vBox.addWidget(normalizerRB)

            groupBox.setLayout(vBox)

            ok = qtWidgets.QPushButton("Ok")
            cancel = qtWidgets.QPushButton("Cancel")

            cancel.clicked.connect(self.normalizeDialog.close)
            ok.clicked.connect(self.getNormalizer)

            buttonLayout.addWidget(cancel)
            buttonLayout.addStretch(1)
            buttonLayout.addWidget(ok)

            dialogBox.addWidget(groupBox)
            dialogBox.addLayout(buttonLayout)

            self.normalizeDialog.setWindowTitle("Normalize raw data")
            self.normalizeDialog.setLayout(dialogBox)
            self.normalizeDialog.resize(250, 250)
            self.normalizeDialog.exec_()

    def getNormalizer(self):
        """This function divides the raw data stored in array TT by the normalizer to normalize it.
        """
        try:
            if self.buttonGroup.checkedId() != -1:
                self.normalizeDialog.close()
                for norm in self.normalizers:
                    if norm.endswith(str(self.buttonGroup.checkedId())):
                        self.normalizer = self.scans[self.scan].data[norm]
                        self.normalizer = np.reshape(self.normalizer, (len(self.normalizer), 1))
                        self.dockedOpt.TT = np.divide(self.dockedOpt.TT, self.normalizer)
                        self.dockedOpt.normalizingStat = True
        except Exception as e:
            qtWidgets.QMessageBox.warning(self.myMainWindow, "Dimension Error", "Please make sure the selected normalizer "
                                                                      "has the same row dimension as the raw data." +
                                                                      "Exception: " + str(e))

    def possibleRawDataLineGraphXAxis(self):
        """This function finds the possible x-axis for the raw data line graph. Also adds Bins to
        the list.
        :return: list of possible x-axis
        """
        linePlotXAxis = []
        for key in self.scans[self.scan].L:
            if key == 'L':
                linePlotXAxis.append(key)
                linePlotXAxis.append(str('Bins'))
                break
            else:
                linePlotXAxis.append(key)
        return linePlotXAxis

    def RawDataLineGraphXAxisDialog(self):
        """Creates a dialog with dynamically coded radio buttons from the spec file, which allow the
        user to select the x-axis for the scan.
        """
        self.xAxisRawDataDialog = qtWidgets.QDialog(self.myMainWindow)
        self.xAxisRawDataDialog.setModal(True)
        dialogBox = qtWidgets.QVBoxLayout()
        buttonLayout = qtWidgets.QHBoxLayout()
        vBox = qtWidgets.QVBoxLayout()

        groupBox = qtWidgets.QGroupBox("Select x-axis")
        self.possibleRawDataXBtnGroup = qtWidgets.QButtonGroup(groupBox)
        xAxis = self.possibleRawDataLineGraphXAxis()
        i = 0
        for x in xAxis:
            xRB = qtWidgets.QRadioButton(x)
            self.possibleRawDataXBtnGroup.addButton(xRB, i)
            vBox.addWidget(xRB)
            i += 1
        groupBox.setLayout(vBox)

        ok = qtWidgets.QPushButton("Ok")

        ok.clicked.connect(self.xAxisRawDataDialog.accept)

        buttonLayout.addStretch(1)
        buttonLayout.addWidget(ok)

        dialogBox.addWidget(groupBox)
        dialogBox.addLayout(buttonLayout)

        self.xAxisRawDataDialog.setWindowTitle("Select x-axis for scan")
        self.xAxisRawDataDialog.setLayout(dialogBox)
        self.xAxisRawDataDialog.resize(200, 100)
        self.xAxisRawDataDialog.exec_()

    def getxAxisForScan(self):
        """This function selects the x-axis depending on what the user selected, as well as other
        criteria for the raw data line graph. Returns a list of zeros if no radio button was selected.
        :return: list of elements to plot the raw data line graph
        """
        self.RawDataLineGraphXAxisDialog()
        while self.xAxisRawDataDialog.result() != self.xAxisRawDataDialog.Accepted:
            self.RawDataLineGraphXAxisDialog()

        if self.xAxisRawDataDialog.result() == self.xAxisRawDataDialog.Accepted and \
                self.possibleRawDataXBtnGroup.checkedId() != -1:
            xAxisList = self.possibleRawDataLineGraphXAxis()
            xAxisInd = self.possibleRawDataXBtnGroup.checkedId()

            xAxisName = xAxisList[xAxisInd]
            if xAxisName == "Bins":
                nRow, nCol = self.dockedOpt.fileInfo()
                x = range(nRow)
            else:
                x = self.scans[self.scan].data[xAxisName]

            self.xAxisRawDataDialog.close()

            return xAxisName, x, self.scan





