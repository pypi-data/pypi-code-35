#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

#C In some methods LFit or L refer to the Lattice Constant not RLU
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

from threading import Timer

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
import pylab as plab
import numpy as np
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from xPlotUtil.Source.DockedOptions import DockedOption

# ---------------------------------------------------------------------------------------------------------------------#

class MainWindow (qtWidgets.QMainWindow):
    """Initializes the main window with the central tab widget. It also has the graphing methods for the raw data and
    creating a report.
    """
    def __init__ (self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setGeometry(50, 50, 1000, 800)
        self.setMinimumSize(800, 700)
        self.setWindowTitle("xPlot Util")
        self.setWindowIcon(qtGui.QIcon('Graph.png'))
        self.dockedOpt = DockedOption(parent=self)
        self.gausFit = self.dockedOpt.gausFit
        self.readSpec = self.dockedOpt.readSpec
        self.algebraExp = self.gausFit.algebraExp
        self.lorentFit = self.dockedOpt.lorentFit
        self.canvasArray = []
        self.figArray = []

        self.SetupComponents()
        self.windowTabs()
        self.dockedOpt.DockMainOptions()
        self.setCentralWidget(self.tabWidget)
        self.setTabPosition(qtCore.Qt.RightDockWidgetArea | qtCore.Qt.LeftDockWidgetArea, qtWidgets.QTabWidget.North)

        self.contrastMax = 0
        self.contrastMin = 0
        self.scan = ""
        self.xAxisName = ""
        self.xAxis = []

    # -----------------------------Central Tab Widget------------------------------------------------------------------#
    def windowTabs(self):
        """This function creates the central widget QTabWidget.
        """
        self.tabWidget = qtWidgets.QTabWidget()

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)


    def closeTab(self, tabIndex):
        """This method closes the tab and closes the canvas. A garbage collector is used
        to collect the left memory.
        :param tabIndex: index of the tab
        """
        self.figArray[tabIndex].clear()
        self.figArray.pop(tabIndex)
        self.canvasArray[tabIndex].renderer.clear()
        del self.canvasArray[tabIndex].renderer
        self.canvasArray[tabIndex].mpl_disconnect(self.canvasArray[tabIndex].scroll_pick_id)
        self.canvasArray[tabIndex].mpl_disconnect(self.canvasArray[tabIndex].button_pick_id)
        self.canvasArray[tabIndex].close()
        self.canvasArray.pop(tabIndex)

        self.tabWidget.removeTab(tabIndex)

    def savingCanvasTabs(self,tab, name, canvas, fig):
        """This method adds the tab widget to the tab widget, and it adds the canvas and fig to arrays.
        :param tab: QWidget
        :param name: name of tab
        :param canvas: graph canvas
        :param fig: graph figure
        """
        self.tabWidget.addTab(tab, name)
        self.tabWidget.setCurrentWidget(tab)

        self.canvasArray.append(canvas)
        self.figArray.append(fig)

    # --------------------------------------Menu Bar and Such----------------------------------------------------------#
    def SetupComponents(self):
        """ Function to setups status bar and menu bar
        """
        self.myStatusBar = qtWidgets.QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.progressBar = qtWidgets.QProgressBar()
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressLabel = qtWidgets.QLabel()
        self.spaceLabel = qtWidgets.QLabel()
        self.myStatusBar.addWidget(self.progressLabel)
        self.myStatusBar.addWidget(self.spaceLabel)
        self.myStatusBar.addWidget(self.progressBar, 1)
        self.spaceLabel.hide()
        self.progressLabel.hide()
        self.progressBar.hide()
        self.myStatusBar.showMessage("Ready", 3000)

        self.CreateActions()
        self.CreateMenus()
        self.fileMenu.addAction(self.openAction)

        self.exportMenu = self.fileMenu.addMenu("Export")
        self.exportMenu.addAction(self.reportAction)
        self.exportMenu.addAction(self.binGausFitReportAction)

        self.fileMenu.addAction(self.resetAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.graphMenu.addAction(self.mainOptionsAction)
        self.graphMenu.addAction(self.normalizeAction)
        self.graphMenu.addAction(self.algebraicExpAction)

        self.fitMenu = self.graphMenu.addMenu("Fits")
        self.fitMenu.addAction(self.gaussianFitAction)
        self.fitMenu.addAction(self.lorentzianFitAction)
        self.fitMenu.addAction(self.voigtFitAction)
        self.fitMenu.addAction(self.latticeFitAction)
        self.graphMenu.addSeparator()
        self.graphMenu.addAction(self.selectScanxAxisAction)
        self.graphMenu.addAction(self.setVoltageAction)

        self.helpMenu.addSeparator()  
        self.helpMenu.addAction(self.aboutAction)

        self.latticeFitAction.setEnabled(False)

    def CreateActions(self):
        """Function that creates the actions used in the menu bar
        """
        self.openAction = qtWidgets.QAction(qtGui.QIcon('openFolder.png'), '&Open', self)
        self.openAction.setShortcut(qtGui.QKeySequence.Open)
        self.openAction.setStatusTip("Open an existing file")
        self.openAction.triggered.connect(self.readSpec.openSpecFile)

        self.exitAction = qtWidgets.QAction(qtGui.QIcon('exit.png'), 'E&xit',
                                        self, shortcut="Ctrl+Q",
                                        statusTip="Exit the Application",
                                        triggered=self.exitFile)
        self.resetAction = qtWidgets.QAction('Reset', self, statusTip="Resets xPlot Util",
                                  triggered=self.dockedOpt.resetxPlot)
        self.reportAction = qtWidgets.QAction('Fit Report', self, statusTip="Create a report of the fit data",
                                         triggered=self.ReportDialog)
        self.binGausFitReportAction = qtWidgets.QAction('Fit of each Bin Report', self, statusTip="Create a report from rach bin "
                                                                                        "fit data.",
                                              triggered=self.gausFit.EachFitDataReport)
        self.mainOptionsAction = qtWidgets.QAction('Main Options', self, statusTip="Main options for xPlot Util",
                                             triggered=self.dockedOpt.restoreMainOptions)
        self.gaussianFitAction= qtWidgets.QAction('Gaussian Fit',self, statusTip="Gaussian fit",
                                        triggered=self.dockedOpt.WhichPeakGaussianFit)
        self.lorentzianFitAction = qtWidgets.QAction('Lorentzian Fit', self, statusTip="Lorentzian fit.",
                                         triggered=self.lorentFit.WhichPeakLorentzianFit)
        self.voigtFitAction = qtWidgets.QAction('Voigt Fit', self, statusTip="Voigt fit.",
                                         triggered=self.lorentFit.WhichPeakVoigtFit)
        self.latticeFitAction = qtWidgets.QAction('Lattice Fit', self, statusTip="Lattice fit.",
                                  triggered =self.dockedOpt.GraphingLatticeOptionsTree)
        self.normalizeAction = qtWidgets.QAction('Normalize', self, statusTip='Normalizes the data',
                                       triggered=self.readSpec.NormalizerDialog)
        self.algebraicExpAction = qtWidgets.QAction('Algebraic Expressions', self, statusTip='Algebraic expressions.',
                                       triggered=self.dockedOpt.DataGraphingAlgebraicExpOptionsTree)
        self.selectScanxAxisAction = qtWidgets.QAction('Set x-Axis', self, statusTip='Select xAxis for scan',
                                                                           triggered=self.selectScanxAxis)
        self.setVoltageAction = qtWidgets.QAction('Set Voltage', self, statusTip='Set the voltage for the fits',
                                             triggered=self.setVoltage)
        self.aboutAction = qtWidgets.QAction(qtGui.QIcon('about.png'), 'A&bout',
                                         self, shortcut="Ctrl+B", statusTip="Displays info about the graph program",
                                         triggered=self.aboutHelp)

    def showProgress(self, txt):
        self.progressBar.show()
        self.progressLabel.show()
        self.spaceLabel.show()

        self.progressLabel.setText(txt)
        self.progressBar.setValue(100)
        stop = Timer(1.5, self.hideProgress)
        stop.start()

    def hideProgress(self):
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.progressLabel.hide()
        self.spaceLabel.hide()

    def CreateMenus(self):
        """This is where I initialize the menu bar and create the menus
        """
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")
        self.graphMenu = self.mainMenu.addMenu("xPlot")
        self.helpMenu = self.mainMenu.addMenu("Help")

    def exitFile(self):
        """Exit method that closes the program.
        """
        response = self.dockedOpt.msgApp("Exiting Form", "Would you like to exit the form")

        if response == "Y":
            self.close()
        else:
            pass

    def aboutHelp(self):
        """Talks briefly about the program.
        """
        """This needs further development. In its infancy level. """
        qtWidgets.QMessageBox.about(self, "About xPlot Util",
                          "Click on the browse button to select and open a spec file. "
                          "The PVvalue files should be under the same directory as the spec. Double click"
                          " on a PVvalue and the file will automatically open. After the file has been open"
                          " the program's fittings and plots will enable.")

    # ----------------------------------------Raw Data Graphs----------------------------------------------------------#
    def PlotColorGraphRawData(self):
        """This function uses the raw data to plot a color graph of the data.
        """
        # Reads file header for voltage
        inF = open(self.dockedOpt.fileName, 'r')
        lines = inF.readlines()
        header = ''
        for (iL, line) in enumerate(lines):
            if line.startswith('#'):
                header = line
        inF.close()
        words = header.split()
        ampl = ''
        if len(words) > 6:
            ampl = words[5]

        line1 = '[-' + str(ampl) + '] --> [0] --> [+' + str(ampl) + '] --> [0] --> [-' + str(ampl) + '] '

        xx = self.xAxis
        if self.xAxisName == "Bins":
            yLabel = "Points"
        else:
            yLabel = self.xAxisName

        gTitle = 'Raw Data Color Graph (Scan#: ' + self.scan + ')'
        statTip = "Raw Data Color Graph"
        xLabel = 'Bins (voltage:' + line1 + ')'
        tabName = 'Raw Data Color Graph'
        whichG = 'C'

        self.GraphUtilRawDataLineGraphs(gTitle, xLabel, yLabel, statTip, tabName, xx, whichG)

    def ColorGraphContrastDialog(self):
        """This method creates a dialog with dynamically created radio buttons from the spec file, which allow the
        user to pick which chamber was used to normalize.
        """
        # if self.dockedOpt.normalizingStat == False and self.dockedOpt.FileError() == False :
        self.contrastDialog = qtWidgets.QDialog(self)
        inputForm = qtWidgets.QFormLayout()
        buttonLayout = qtWidgets.QHBoxLayout()
        hBox = qtWidgets.QHBoxLayout()
        hBox1 = qtWidgets.QHBoxLayout()

        maxContrastLbl = qtWidgets.QLabel("Max Intensity:")
        self.maxContrastSpin = qtWidgets.QDoubleSpinBox()
        self.maxContrastSpin.setMaximum(np.max(self.dockedOpt.TT) + 1000)
        self.maxContrastSpin.setMinimum(np.min(self.dockedOpt.TT) - 999)
        self.maxContrastSpin.setValue(np.max(self.dockedOpt.TT))
        self.maxContrastSpin.valueChanged.connect(self.ContrastSpinMaxValue)
        self.contrastMax = self.maxContrastSpin.value()
        self.maxContrastSlider = qtWidgets.QSlider(qtCore.Qt.Horizontal)
        self.maxContrastSlider.setMaximum(np.max(self.dockedOpt.TT) + 1000)
        self.maxContrastSlider.setMinimum(np.min(self.dockedOpt.TT) - 999)
        self.maxContrastSlider.setValue(np.max(self.dockedOpt.TT))
        self.maxContrastSlider.valueChanged.connect(self.maxContrastSpin.setValue)

        minContrastLbl = qtWidgets.QLabel("Min Intensity: ")
        self.minContrastSpin = qtWidgets.QDoubleSpinBox()
        self.minContrastSpin.setMaximum(np.max(self.dockedOpt.TT) + 999)
        self.minContrastSpin.setMinimum(np.min(self.dockedOpt.TT) - 1000)
        self.minContrastSpin.setValue(np.min(self.dockedOpt.TT))
        self.minContrastSpin.valueChanged.connect(self.ContrastSpinMinValue)
        self.contrastMin = self.minContrastSpin.value()
        self.minContrastSlider = qtWidgets.QSlider(qtCore.Qt.Horizontal)
        self.minContrastSlider.setMaximum(np.max(self.dockedOpt.TT) + 999)
        self.minContrastSlider.setMinimum(np.min(self.dockedOpt.TT) - 1000)
        self.minContrastSlider.setValue(np.min(self.dockedOpt.TT))
        self.minContrastSlider.valueChanged.connect(self.minContrastSpin.setValue)
        self.minContrastSlider.setTickInterval(4)

        hBox.addWidget(maxContrastLbl)
        hBox.addWidget(self.maxContrastSpin)
        hBox.addWidget(self.maxContrastSlider)
        hBox1.addWidget(minContrastLbl)
        hBox1.addWidget(self.minContrastSpin)
        hBox1.addWidget(self.minContrastSlider)

        okBtn = qtWidgets.QPushButton("Ok")
        okBtn.clicked.connect(self.ReplottingColorGraph)
        cancelBtn = qtWidgets.QPushButton("Cancel")
        cancelBtn.clicked.connect(self.contrastDialog.close)

        buttonLayout.addWidget(cancelBtn)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okBtn)

        inputForm.addRow(hBox)
        inputForm.addRow(hBox1)
        inputForm.addRow(buttonLayout)

        self.contrastDialog.setWindowTitle("Adjust contrast")
        self.contrastDialog.setLayout(inputForm)
        self.contrastDialog.resize(300, 100)
        self.contrastDialog.exec_()

    def ContrastSpinMinValue(self, value):
        if value >= self.maxContrastSpin.value():
            self.minContrastSpin.setValue(self.contrastMin)
            self.minContrastSlider.setValue(self.contrastMin)
        else:
            self.contrastMin = value

    def ContrastSpinMaxValue(self, value):
        if value <= self.minContrastSpin.value():
            self.maxContrastSpin.setValue(self.contrastMax)
            self.maxContrastSlider.setValue(self.contrastMax)
        else:
            self.contrastMax = value

    def ReplottingColorGraph(self):
        self.contrastDialog.close()
        max = self.maxContrastSpin.value()
        min = self.minContrastSpin.value()
        ind = self.tabWidget.currentIndex()
        self.figArray[ind].clear()
        axes = self.figArray[ind].add_subplot(111)
        nRow = self.dockedOpt.TT.shape[0]
        nCol = self.dockedOpt.TT.shape[1]

        z = np.linspace(min, max)
        xx = self.xAxis
        yy = range(nCol)
        axes.contourf(yy, xx, self.dockedOpt.TT, z, cmap='jet')
        self.figArray[ind].colorbar(axes.contourf(yy, xx, self.dockedOpt.TT, z, cmap='jet'))
        gTitle = 'Raw Data Color Graph (Scan#: ' + self.readSpec.scan + ')'
        xLabel = 'Bins'
        yLabel = self.xAxisName
        axes.set_title(gTitle)
        axes.set_xlabel(xLabel)
        axes.set_ylabel(yLabel)
        self.canvasArray[ind].draw()

    def GraphUtilRawDataLineGraphs(self, gTitle, xLabel, yLabel, statTip, tabName, xx, whichG):
        """Generic graph method that helps graph the raw data.
        :param gTitle: Title of the graph
        :param xLabel: x-axis label
        :param yLabel: y-axis label
        :param statTip: status tip
        :param tabName: tab name
        :param xx: x-axis values
        :param whichG: char to know which graph to plot
        """
        mainGraph = qtWidgets.QWidget()
        fig = plab.Figure((3.0, 3.0), dpi=100)
        canvas = FigureCanvas(fig)

        canvas.setParent(mainGraph)
        axes = fig.add_subplot(111)

        nRow = self.dockedOpt.TT.shape[0]  # Gets the number of rows
        nCol = self.dockedOpt.TT.shape[1]

        if whichG == 'L':
            for j in range(nCol):
                yy = self.dockedOpt.TT[:, j]
                axes.plot(xx, yy)
        elif whichG == 'C':
            tMax = np.max(self.dockedOpt.TT)
            tMin = np.min(self.dockedOpt.TT)
            z = np.linspace(tMin, tMax)
            yx = range(nCol)

            axes.contourf(yx, xx, self.dockedOpt.TT, z, cmap='jet')
            fig.colorbar(axes.contourf(yx, xx, self.dockedOpt.TT, z, cmap='jet'))

            contrastBtn = qtWidgets.QPushButton("Contrast")
            contrastBtn.clicked.connect(self.ColorGraphContrastDialog)

        axes.set_title(gTitle)
        axes.set_xlabel(xLabel)
        axes.set_ylabel(yLabel)
        canvas.draw()

        tab = qtWidgets.QWidget()
        tab.setStatusTip(statTip)
        vbox = qtWidgets.QVBoxLayout()
        graphNavigationBar = NavigationToolbar(canvas, self)
        vbox.addWidget(graphNavigationBar)
        if whichG == 'C':
            hBox = qtWidgets.QHBoxLayout()
            hBox.addStretch()
            hBox.addWidget(contrastBtn)
            vbox.addLayout(hBox)
        vbox.addWidget(canvas)
        tab.setLayout(vbox)

        self.savingCanvasTabs(tab, tabName, canvas, fig)

    def PlotLineGraphRawData(self):
        """This method graphs the raw data into a line graph with the x-axis the user picks.
        """
        xAxis, xx, scan = self.getScanxAxis()

        if xAxis != 0:
            if xAxis == 'L':
                gTitle = 'Raw Data in RLU (Scan#: ' + scan + ')'
                xLabel = 'RLU (Reciprocal Lattice Unit)'
                statTip = 'Raw Data in RLU (Reciprocal Lattice Unit)'
                tabName = 'Raw Data (RLU)'
            elif xAxis == 'Bins':
                gTitle = 'Raw Data in Bins (Scan#: ' + scan + ')'
                xLabel = 'Points'
                statTip = 'Raw Data in Bins'
                tabName = 'Raw Data (Bins)'
            else:
                gTitle = 'Raw Data in ' + xAxis + ' (Scan#: ' + scan + ')'
                xLabel = xAxis
                statTip = 'Raw Data in ' + xAxis
                tabName = 'Raw Data (' + xAxis + ')'

            self.GraphUtilRawDataLineGraphs(gTitle, xLabel, 'Intensity', statTip, tabName, xx, 'L')

    # -----------------------------------Creating Report---------------------------------------------------------------#
    def ReportButton(self):
        """This button creates a report.
        """
        self.reportBtn = qtWidgets.QPushButton('Fit Report', self)
        self.reportBtn.setStatusTip("Creates a report of the chosen data.")
        self.reportBtn.clicked.connect(self.CreateReport)

    def CancelReportButton(self):
        """This button cancels the creation of a report.
        """
        self.cancelReportBtn = qtWidgets.QPushButton('Cancel', self)
        self.cancelReportBtn.setStatusTip("Cancels the creation of the report.")
        self.cancelReportBtn.clicked.connect(self.reportDialog.close)

    def CreateReport(self):
        """This method calls on the save file dialog and once the file has been selected it writes out the report.
        """
        if self.reportCbGausFit.isChecked() or self.reportCbLFit.isChecked():
            self.reportDialog.close()
            selectedFilters = ".txt"
            self.reportFile, self.reportFileFilter = qtWidgets.QFileDialog.getSaveFileName(self, "Save Report", "",
                                                                                 selectedFilters)
            if self.reportFile != "":
                self.reportFile += self.reportFileFilter
                self.WritingReport()

    def ReportDialog(self):
        """Dialog that allows the user to select the data it wants on the report.
        """
        self.reportDialog = qtWidgets.QDialog(self)
        vBox = qtWidgets.QVBoxLayout()
        buttonLayout = qtWidgets.QHBoxLayout()

        self.ReportCheckBox()
        self.CancelReportButton()
        self.ReportButton()

        buttonLayout.addWidget(self.cancelReportBtn)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.reportBtn)

        vBox.addWidget(self.reportGroupBx)
        vBox.addLayout(buttonLayout)

        self.reportDialog.setWindowTitle("Create Final Report")
        self.reportDialog.setLayout(vBox)
        self.reportDialog.exec_()

    def ReportCheckBox(self):
        """This method creates the check boxes used in the report dialog.
        """
        self.reportGroupBx = qtWidgets.QGroupBox("Select the data")

        self.reportCbGausFit = qtWidgets.QCheckBox("Gaussian Fit")
        self.reportCbLFit = qtWidgets.QCheckBox("Lattice Fit")
        self.reportCbGausFit.setEnabled(False)
        self.reportCbLFit.setEnabled(False)

        if self.dockedOpt.fitStat == True:
            self.reportCbGausFit.setEnabled(True)
        if self.dockedOpt.LFitStat == True:
            self.reportCbLFit.setEnabled(True)

        vbox = qtWidgets.QVBoxLayout()
        vbox.addWidget(self.reportCbGausFit)
        vbox.addWidget(self.reportCbLFit)

        self.reportGroupBx.setLayout(vbox)

    def WritingReport(self):
        """This method writes the data to the report file, calling on the appropriate methods. It's important to
        note that the report can only contain data from the gaussian fit and the lattice fit.
        """
        _, nCol = self.dockedOpt.fileInfo()
        reportData = np.zeros((nCol, 0))
        header = "#H "
        scanNum = self.readSpec.scan
        comment = "#C PVvalue #" + scanNum + "\n"

        if self.reportCbGausFit.isChecked():
            if self.dockedOpt.onePeakStat == True:
                header += "Amp Err Position Err Width Err "
                reportData = np.concatenate((reportData, self.gausFit.OnePkFitData), axis=1)
            if self.dockedOpt.twoPeakStat == True:
                header += "Amp Err Amp Err Pos Err Pos Err Wid Err Wid Err "
                reportData = np.concatenate((reportData, self.gausFit.TwoPkGausFitData), axis=1)

        if self.reportCbLFit.isChecked():
            if self.dockedOpt.onePeakStat == True:
                header += "Lattice Lattice% "
                # Reshapes the array so that it can be append
                L = np.reshape(self.gausFit.LPosData, (len(self.gausFit.LPosData), 1))  # Enables array to be appended
                LPrc = np.reshape(self.gausFit.LPosPrcChangeData, (len(self.gausFit.LPosPrcChangeData), 1))
                reportData = np.concatenate((reportData, L, LPrc), axis=1)
            if self.dockedOpt.twoPeakStat == True:
                header += "Lattice1 Lattice2 Lattice1% Lattice2% "
                L1 = np.reshape(self.gausFit.LPos1Data, (len(self.gausFit.LPos1Data), 1))  # Reshapes to append
                L2 = np.reshape(self.gausFit.LPos2Data, (len(self.gausFit.LPos2Data), 1))  # Reshapes to append
                L1Prc = np.reshape(self.gausFit.LPos1PrcChangeData, (len(self.gausFit.LPos1PrcChangeData), 1))
                L2Prc = np.reshape(self.gausFit.LPos2PrcChangeData, (len(self.gausFit.LPos2PrcChangeData), 1))

                reportData = np.concatenate((reportData, L1, L2, L1Prc, L2Prc), axis=1)

        # Writes to sheet
        np.savetxt(self.reportFile, reportData, fmt=str('%f'), header=header, comments=comment)

    def selectScanxAxis(self):
        if self.dockedOpt.TT.any():
            self.xAxisName, self.xAxis, self.scan = self.readSpec.getxAxisForScan()

    def getScanxAxis(self):
        return self.xAxisName, self.xAxis, self.scan

    def setVoltage(self):
        self.gausFit.setVoltage()

def main():
    """Main method.
    """
    app = qtWidgets.QApplication(plab.sys.argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    plab.sys.exit(app.exec_())


if __name__.endswith('__main__'):
    main()