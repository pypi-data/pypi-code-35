import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

from picviewer.controller.slice_controller import SliceController
from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot
from picviewer.controller.combobox_controller import ComboboxController

class PanelController():
    """
        panel control class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow

        self.slicecontroller = SliceController(self.main)

        # Data collect class
        self.collectdata = DataCollector(self.main)
        # Plot class
        self.prepareplot = PreparePlot(self.main)


    def SetPanelButtons(self):
        """
        Create panel buttons
        """

        self.main.panelbuttons = {}
        self.main.panellayout = QtWidgets.QWidget(self.main.centralwidget)
        # Assign button locations
        button_height = 580
        button_left = 160
        x0 = -20*(self.main.ncolumn-2)+button_left
        w0 = 25*(self.main.ncolumn-2)+50
        y0 = (10./3)*(self.main.nrow-2)+button_height
        h0 = 20*(self.main.nrow-2)+60
        self.main.panellayout.setGeometry(QtCore.QRect(x0, y0, w0, h0))
        self.main.gridLayout = QtWidgets.QGridLayout(self.main.panellayout)
        self.main.gridLayout.setContentsMargins(0, 0, 0, 0)
        
        for i in np.arange(self.main.nrow):
            for j in np.arange(self.main.ncolumn):
                self.main.panelbuttons[(i,j)] = QtWidgets.QRadioButton(self.main.panellayout)
                self.main.panelbuttons[(i,j)].setStyleSheet("")
                self.main.panelbuttons[(i,j)].setText("")
                self.main.gridLayout.addWidget(self.main.panelbuttons[(i,j)], i, j, 1, 1)
        self.main.panellayout.show()      
        
        i = (self.main.panelselect-1)/self.main.ncolumn
        j = np.mod((self.main.panelselect-1),self.main.ncolumn)
        self.main.panelbuttons[(i,j)].setChecked(True)


    def panelbutton(self):
        """
        Change the parameters to the saved ones in the selected panel

        """
        # self.panelselect is the index of a selected panel, i.e., 1, 2, 3, or ...
        for i in np.arange(self.main.nrow):
            for j in np.arange(self.main.ncolumn):
                if self.main.panelbuttons[(i,j)].isChecked():
                    self.main.panelselect = i*self.main.ncolumn+j+1

        panelselect = self.main.panelselect
        # i.e., self.main.field_select_panel = [True, True, False, ....]
        if self.main.field_select_panel[panelselect-1]:
            self.main.fieldButton.setChecked(True)
        else:
            self.main.particleButton.setChecked(True)

        # i.e., self.main.field_panel = ['Bx', 'By', ...]
        field = self.main.field_panel[panelselect-1]
        index = self.main.field_list_indexed[field]
        self.main.fieldsComboBox.setCurrentIndex(index)
        # i.e., self.species_panel = ['elec', 'ions', ...]
        if self.main.species_list:
            species = self.main.species_panel[panelselect-1]
            index = self.main.species_list_indexed[species]
            self.main.speciesComboBox.setCurrentIndex(index)
     
        # i.e., phase = ['px','x'], ['x','z'], ...
        phase = self.main.phase_panel[panelselect-1]        
        if self.main.dim == 2:
            index = self.main.phase_list1_indexed[phase]
            self.main.phaseComboBox.setCurrentIndex(index)
        else:
            if self.main.sliceplane_panel[panelselect-1] == 'yx':
                index = self.main.phase_list2_indexed[phase]
                self.main.phaseComboBox.clear() 
                for i in np.arange(len(self.main.phase_list2)):
                    self.main.phaseComboBox.addItem(
                        self.main.phase_list2[i][0]+'-'+self.main.phase_list2[i][1], i)

            elif self.main.sliceplane_panel[panelselect-1] == 'xz':
                index = self.main.phase_list1_indexed[phase]
                self.main.phaseComboBox.clear()
                for i in np.arange(len(self.main.phase_list1)):
                    self.main.phaseComboBox.addItem(
                        self.main.phase_list1[i][0]+'-'+self.main.phase_list1[i][1], i)

            elif self.main.sliceplane_panel[panelselect-1] == 'yz':
                index = self.main.phase_list3_indexed[phase]
                self.main.phaseComboBox.clear() 
                for i in np.arange(len(self.main.phase_list3)):
                    self.main.phaseComboBox.addItem(
                        self.main.phase_list3[i][0]+'-'+self.main.phase_list3[i][1], i)
            self.main.phaseComboBox.setCurrentIndex(index)

        amrlevel = self.main.amrlevel_panel[panelselect-1]
        self.main.amrSpinBox.setValue(amrlevel)

        if self.main.aspect_panel[panelselect-1] == 'equal':
            self.main.aspectCheckBox.setChecked(True)
        else:
             self.main.aspectCheckBox.setChecked(False)

        if self.main.line_panel[panelselect-1] == True:
            self.main.lineCheckBox.setChecked(True)
        else:
            self.main.lineCheckBox.setChecked(False)

        if self.main.rectangle_panel[panelselect-1] == True:
            self.main.rectangleCheckBox.setChecked(True)
        else:
            self.main.rectangleCheckBox.setChecked(False)

        contrast = self.main.contrast_panel[panelselect-1]
        self.main.contrastSlider.setValue(contrast)
        self.main.contrastLabel.setText(str("%d%%" %contrast))
        
        
        if self.main.dim == 3:
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            yaxis = self.main.yaxis_dic[tstep-1]
            zaxis = self.main.zaxis_dic[tstep-1]
            # i.e., self.main.slicevalue_panel = [0, 0, 10, .. ] 
            # The number is between [0,50] and specifies the location
            # on the 3rd axis of the 2D slice plane.
            slicevalue = self.main.slicevalue_panel[self.main.panelselect-1]
            stride = self.main.stride_panel[self.main.panelselect-1]
            self.main.slicevalueSlider.setValue(slicevalue)
            self.main.strideSlider.setValue(stride)
            if self.main.sliceplane_panel[self.main.panelselect-1] == 'yx':
                self.main.xyButton.setChecked(True)
                zvalue = zaxis[0]+(zaxis[-1]-zaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("z=%.2f" %zvalue))   
                self.main.strideLabel.setText(u'\u0394'+ "z=%.2f" %(stride/50.)) 

            elif self.main.sliceplane_panel[self.main.panelselect-1] == 'xz':
                self.main.xzButton.setChecked(True)
                yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("y=%.2f" %yvalue))
                self.main.strideLabel.setText(u'\u0394'+ "y=%.2f" %(stride/50.))

            elif self.main.sliceplane_panel[self.main.panelselect-1] == 'yz':
                self.main.xzButton.setChecked(True)
                xvalue = xaxis[0]+(xaxis[-1]-xaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("x=%.2f" %xvalue))
                self.main.strideLabel.setText(u'\u0394'+ "x=%.2f" %(stride/50.))

        if self.main.rectangleCheckBox.isChecked():
            ComboboxController(self.main).setlocalcombobox()

        # update x1min,x1max, x2min, x2max lables
        self.slicecontroller.ChangeRangeSliderLabels()

        # change tstep lable
        tstep = self.main.tstep_panel[self.main.panelselect-1]
        self.main.time = self.main.taxis[tstep-1]
        self.main.tstepLabel.setText("tstep %d" %tstep)
        self.main.timeLabel.setText("%6.1f fs" %self.main.time)
        self.main.timeSlider.setValue(tstep)


    def RecreatePanelButton(self):

        try:
            species_list = self.main.species_list
            lparticle = 1
        except AttributeError:
            lparticle = 0

        # when select different numbers of columns or rows
        nrow = self.main.rowpanelSpinBox.value()
        ncolumn = self.main.columnpanelSpinBox.value()
        # save old nrow and ncolumn
        nrow0 = self.main.nrow; ncolumn0 = self.main.ncolumn
        # update nrow and ncolumn
        self.main.nrow = nrow
        self.main.ncolumn = ncolumn
        # delete old panel buttons
        self.main.panellayout.deleteLater()

        if self.main.panelselect > (self.main.nrow*self.main.ncolumn): 
            # This is when the panel dimension is decreased.
            self.main.panelselect = self.main.nrow*self.main.ncolumn
        
        # Create new panel buttons
        self.SetPanelButtons()

        tstep_panel0 = self.main.tstep_panel
        field_select_panel0 = self.main.field_select_panel
        field_panel0 = self.main.field_panel
        species_panel0 = self.main.species_panel
        phase_panel0 = self.main.phase_panel
        line_panel0 = self.main.line_panel
        rectangle_panel0 = self.main.rectangle_panel
        aspect_panel0 = self.main.aspect_panel
        amrlevel_panel0 = self.main.amrlevel_panel
        contrast_panel0 = self.main.contrast_panel
        if self.main.dim  == 3:
            sliceplane_panel0 = self.main.sliceplane_panel
            slicevalue_panel0 = self.main.slicevalue_panel
            stride_panel0 = self.main.stride_panel
        xminloc_panel0 = self.main.xminloc_panel
        xmaxloc_panel0 = self.main.xmaxloc_panel
        if self.main.dim  == 3:
            yminloc_panel0 = self.main.yminloc_panel
            ymaxloc_panel0 = self.main.ymaxloc_panel
        zminloc_panel0 = self.main.zminloc_panel
        zmaxloc_panel0 = self.main.zmaxloc_panel
        localfield_panel0 = self.main.localfield_panel
        localphase_panel0 = self.main.localphase_panel
        
        # Re-initialize the panel parameter lists.
        self.main.tstep_panel = []
        self.main.field_panel = []
        self.main.species_panel = []
        self.main.phase_panel = []
        self.main.line_panel = []
        self.main.field_select_panel = []
        self.main.rectangle_panel = []
        self.main.aspect_panel = []
        self.main.sliceplane_panel = []
        self.main.slicevalue_panel = []
        self.main.contrast_panel = []
        self.main.stride_panel = []
        self.main.xminloc_panel = []
        self.main.xmaxloc_panel = []
        self.main.yminloc_panel = []
        self.main.ymaxloc_panel = []
        self.main.zminloc_panel = []
        self.main.zmaxloc_panel = []
        self.main.localfield_panel = []
        self.main.localphase_panel = []
        self.main.amrlevel_panel = []


        for l in np.arange(self.main.nrow*self.main.ncolumn):
            self.main.field_panel.append(field_panel0[np.mod(l,nrow0*ncolumn0)])
            if l < nrow0*ncolumn0:
                self.main.tstep_panel.append(tstep_panel0[l])
                self.main.field_select_panel.append(field_select_panel0[l])
                self.main.line_panel.append(line_panel0[l])
                self.main.rectangle_panel.append(rectangle_panel0[l])
                self.main.aspect_panel.append(aspect_panel0[l])
                #if self.main.species_list:
                if lparticle:
                    self.main.species_panel.append(species_panel0[l])
                    self.main.phase_panel.append(phase_panel0[l])
                    self.main.localphase_panel.append(localphase_panel0[l])
                self.main.contrast_panel.append(contrast_panel0[l])
                self.main.localfield_panel.append(localfield_panel0[l])
                if self.main.dim == 3:
                    self.main.sliceplane_panel.append(sliceplane_panel0[l])
                    self.main.slicevalue_panel.append(slicevalue_panel0[l])
                    self.main.stride_panel.append(stride_panel0[l])
                self.main.xminloc_panel.append(xminloc_panel0[l])
                self.main.xmaxloc_panel.append(xmaxloc_panel0[l])
                if self.main.dim == 3:
                    self.main.yminloc_panel.append(yminloc_panel0[l])
                    self.main.ymaxloc_panel.append(ymaxloc_panel0[l])
                self.main.zminloc_panel.append(zminloc_panel0[l])
                self.main.zmaxloc_panel.append(zmaxloc_panel0[l])
                self.main.amrlevel_panel.append(amrlevel_panel0[l])
            else:
                self.main.tstep_panel.append(len(self.main.taxis))
                self.main.field_select_panel.append('True')
                self.main.line_panel.append(False)
                self.main.rectangle_panel.append(False)
                self.main.aspect_panel.append('auto')
                #if self.main.species_list:
                if lparticle:
                    self.main.species_panel.append(species_panel0[0])
                    self.main.phase_panel.append(self.main.phase_list1[0])
                    self.main.localphase_panel.append(self.main.localphase_list1[0])
                self.main.contrast_panel.append(100)
                self.main.localfield_panel.append(self.main.localfield_list[0])
                if self.main.dim == 3:
                    self.main.sliceplane_panel.append('xz')
                    self.main.slicevalue_panel.append(25)
                    self.main.stride_panel.append(10)
                self.main.xminloc_panel.append(0)
                self.main.xmaxloc_panel.append(100)
                if self.main.dim == 3:
                    self.main.yminloc_panel.append(0)
                    self.main.ymaxloc_panel.append(100)
                self.main.zminloc_panel.append(0)
                self.main.zmaxloc_panel.append(100)
                self.main.amrlevel_panel.append(0)
                
                
        self.main.figure.clear()

        self.collectdata.loaddatasync()
        self.prepareplot.plotsync()

        # Re-create local selection tool variables in each panel
        self.main.resize = np.arange(self.main.nrow*self.main.ncolumn)
        self.main.translate = np.arange(self.main.nrow*self.main.ncolumn)
        self.main.xc = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.yc = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.xcenter = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.ycenter = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.rectw = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.recth = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.xini = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.yini = np.zeros(self.main.nrow*self.main.ncolumn)
    
