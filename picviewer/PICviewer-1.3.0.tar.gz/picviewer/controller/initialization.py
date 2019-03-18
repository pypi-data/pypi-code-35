import os, glob
#from PySide import QtCore, QtGui
import numpy as np

from picviewer.dataloader.get_datainfo import DataInfo
from picviewer.controller.greeting import Greeting

class Initialization():
    """
        Initialization after reading data information
    """
    def __init__(self, Mainwindow):

        self.main = Mainwindow

        # get data information
        self.datainfo = DataInfo()
        param_dic = self.datainfo.datainfo(self.main.filepath)

        self.main.iterations = param_dic['iterations']
        self.main.dataformat = param_dic['dataformat']

        if self.main.dataformat == 'WarpX':
            amrlevel = param_dic['amrlevel']
        else:
            amrlevel = 0
        self.main.amrlevel = amrlevel
        self.main.amrSpinBox.setMaximum(amrlevel)

        self.main.dim = param_dic['dim']
        self.main.coord_system = param_dic['coord_system']
        self.main.xaxis_dic = param_dic['xaxis_dic']
        self.main.yaxis_dic = param_dic['yaxis_dic']
        self.main.zaxis_dic = param_dic['zaxis_dic']
 
        self.main.taxis = param_dic['taxis']
        tstep = len(self.main.iterations)
        xaxis = self.main.xaxis_dic[tstep-1]
        yaxis = self.main.yaxis_dic[tstep-1]
        zaxis = self.main.zaxis_dic[tstep-1]

        self.main.dxfact = param_dic['dxfact']
        self.main.dzfact = param_dic['dzfact']
        self.main.dyfact = param_dic['dyfact']

        try:
            self.main.numpart_list = param_dic['numpart_list']
            lparticle = 1
        except KeyError:
            lparticle = 0
        
        self.main.field_list = param_dic['field_list']
        
        if lparticle:
            self.main.dpfact = param_dic['dpfact_list'] 
            self.main.species_list = param_dic['species_list']
            self.main.phase_list1 = param_dic['phase_list1']
            if self.main.dim == 3:
                self.main.phase_list2 = param_dic['phase_list2']
                self.main.phase_list3 = param_dic['phase_list3']

            self.main.mass_list = param_dic['mass_list']

        # set up local phase list
        self.main.localfield_list = ['field','FFT']

        if lparticle:
            self.main.localphase_list1 = []
            for i in np.arange(len(self.main.phase_list1)):
                if i == 1:
                    self.main.localphase_list1.append(('fE','loglin'))
                    self.main.localphase_list1.append(('fE','loglog'))
                self.main.localphase_list1.append(self.main.phase_list1[i])

            if self.main.dim == 3:
                self.main.localphase_list2 = []
                self.main.localphase_list3 = []
                for i in np.arange(len(self.main.phase_list2)):
                    if i == 1:
                        self.main.localphase_list2.append(('fE','loglin'))
                        self.main.localphase_list2.append(('fE','loglog'))
                    self.main.localphase_list2.append(self.main.phase_list2[i])

                for i in np.arange(len(self.main.phase_list3)):
                    if i == 1:
                        self.main.localphase_list3.append(('fE','loglin'))
                        self.main.localphase_list3.append(('fE','loglog'))
                    self.main.localphase_list3.append(self.main.phase_list3[i])

        # dictionary, i.e., {'Bx':0, 'By':1, ...}
        # For example, we change a panel where 'Bx' is selected. 
        # The combox-box is updated by the index of 'Bx'(see combbobox-controller.py)
        self.main.field_list_indexed = \
                {self.main.field_list[k]: k for k in np.arange(len(self.main.field_list))}

        if lparticle:
            self.main.species_list_indexed = \
                    {self.main.species_list[k]: k for k in np.arange(len(self.main.species_list))}
            self.main.phase_list1_indexed = \
                    {self.main.phase_list1[k]: k for k in np.arange(len(self.main.phase_list1))}
            if self.main.dim == 3:
                self.main.phase_list2_indexed = \
                    {self.main.phase_list2[k]: k for k in np.arange(len(self.main.phase_list2))}
                self.main.phase_list3_indexed = \
                    {self.main.phase_list3[k]: k for k in np.arange(len(self.main.phase_list3))}
            self.main.mass_list_indexed = \
                    {self.main.mass_list[k]: k for k in np.arange(len(self.main.mass_list))}


        # dictionary, i.e., {'field':0, 'FFT':1, ...}
        # For example, we change a panel where local plot 'FFT' is selected. 
        # The combox-box is updated by the index of the 'FFT'
        self.main.localfield_list_indexed = \
                {self.main.localfield_list[k]: k for k in np.arange(len(self.main.localfield_list))}

        if lparticle:
            self.main.localphase_list1_indexed = \
                    {self.main.localphase_list1[k]: k for k in np.arange(len(self.main.localphase_list1))}
            if self.main.dim == 3:
                self.main.localphase_list2_indexed = \
                    {self.main.localphase_list2[k]: k for k in np.arange(len(self.main.localphase_list2))}
                self.main.localphase_list3_indexed = \
                    {self.main.localphase_list3[k]: k for k in np.arange(len(self.main.localphase_list3))}

        # display simulation type
        self.main.simuLabel.setText('%dD %s'%(self.main.dim, self.main.dataformat))
        self.main.coordinateLabel.setText(self.main.coord_system)

        # time step slider
        self.main.tstepLabel.setText("tstep %d" %(len(self.main.iterations)))
        self.main.timeLabel.setText("%6.1f fs" % self.main.taxis[-1])
        self.main.timeSlider.setRange(1,len(self.main.iterations))
        self.main.timeSlider.setSingleStep(1)
        self.main.timeSlider.setValue(len(self.main.iterations))

        # time interval spinbox
        self.main.tiniSpinBox.setMinimum(1)
        self.main.tiniSpinBox.setMaximum(len(self.main.iterations))
        self.main.tiniSpinBox.setValue(np.min([2,len(self.main.iterations)]))
        self.main.tmaxSpinBox.setMinimum(1)
        self.main.tmaxSpinBox.setMaximum(len(self.main.iterations))
        self.main.tmaxSpinBox.setValue(len(self.main.iterations))
        
        # space range slider
        self.main.x1min.setText("zmin")
        self.main.x1minLabel.setText(str("%.1f"%(zaxis[0])))
        self.main.x1max.setText("zmax")
        self.main.x1maxLabel.setText(str("%.1f"%(zaxis[-1])))
        self.main.x2min.setText("xmin")
        self.main.x2minLabel.setText(str("%.1f"%(xaxis[0])))
        self.main.x2max.setText("xmax")
        self.main.x2maxLabel.setText(str("%.1f"%(xaxis[-1])))

        # field combo-boxes
        for i in np.arange(len(self.main.field_list)):
            self.main.fieldsComboBox.addItem(self.main.field_list[i], i)
        self.main.fieldsComboBox.setCurrentIndex(0)
        
        if lparticle:
            # species combo-boxes
            for i in np.arange(len(self.main.species_list)):
                self.main.speciesComboBox.addItem(self.main.species_list[i], i)
            self.main.speciesComboBox.setCurrentIndex(0)
        
            # phase combo-boxes
            for i in np.arange(len(self.main.phase_list1)):
                self.main.phaseComboBox.addItem(
                    self.main.phase_list1[i][0]+'-'+self.main.phase_list1[i][1], i)
            self.main.phaseComboBox.setCurrentIndex(0)


        #########################################################
        # initialize parameters in each panel
        #########################################################
        for l in np.arange(self.main.nrow*self.main.ncolumn):
            
            self.main.tstep_panel.append(tstep)
            self.main.field_select_panel.append(True)
            self.main.field_panel.append(self.main.field_list[np.mod(l,len(self.main.field_list))])


            if lparticle:
                if self.main.species_list:
                    self.main.species_panel.append(self.main.species_list[0])
                self.main.phase_panel.append(self.main.phase_list1[0])
            self.main.line_panel.append(False)
            self.main.rectangle_panel.append(False)
            self.main.aspect_panel.append('auto')
            self.main.xminloc_panel.append(0)
            self.main.xmaxloc_panel.append(100)
            self.main.zminloc_panel.append(0)
            self.main.zmaxloc_panel.append(100)
            self.main.contrast_panel.append(100)
            self.main.localfield_panel.append(self.main.localfield_list[0])

            if lparticle:
                self.main.localphase_panel.append(self.main.localphase_list1[0])
            self.main.amrlevel_panel.append(0)
    
            if self.main.dim == 3:
                self.main.sliceplane_panel.append('xz')
                self.main.slicevalue_panel.append(25)
                self.main.stride_panel.append(10)
                self.main.yminloc_panel.append(0)
                self.main.ymaxloc_panel.append(100)

        if self.main.dim == 3:
            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            yaxis = self.main.yaxis_dic[tstep-1]
            slicevalue= self.main.slicevalue_panel[panelselect-1]
            yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*slicevalue/50.
            self.main.slicevalueLabel.setText(str("y=%.2f" %yvalue))
            stride = self.main.stride_panel[panelselect-1]
            self.main.strideLabel.setText(u'\u0394'+ "y=%.2f" %(stride/50.))

        
        Greeting(self.main)