import numpy as np

from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot

from picviewer.dataplotter.subwindow import SubWindow
from picviewer.dataplotter.prepare_localplot import PrepareLocalPlot

class ComboboxController():
    """
        combobox control class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow

        # colletc data class
        self.collectdata = DataCollector(self.main)
        # prepare data class
        self.prepareplot = PreparePlot(self.main)

    def fieldbutton(self):

        self.main.field_select_panel[self.main.panelselect-1] = True

        self.collectdata.loadfield()
        self.prepareplot.plotfield()

        if self.main.rectangleCheckBox.isChecked():
            self.setlocalcombobox()
            
    def fieldcombobox(self):

        self.main.fieldButton.setChecked(True)
        self.main.field_select_panel[self.main.panelselect-1] = True
        index=self.main.fieldsComboBox.currentIndex()
        self.main.field_panel[self.main.panelselect-1] = self.main.field_list[index]

        self.collectdata.loadfield()
        self.prepareplot.plotfield()

        self.setlocalcombobox()

        if self.main.rectangleCheckBox.isChecked():
            self.setlocalcombobox()

    def particlebutton(self):
   
        self.main.field_select_panel[self.main.panelselect-1] = False

        self.collectdata.loadparticle()
        self.prepareplot.plotparticle()

        if self.main.rectangleCheckBox.isChecked():
            self.setlocalcombobox()

    def speciescombobox(self):

        self.main.particleButton.setChecked(True)
        self.main.field_select_panel[self.main.panelselect-1] = False
        index=self.main.speciesComboBox.currentIndex()
        self.main.species_panel[self.main.panelselect-1] = self.main.species_list[index]

        self.collectdata.loadparticle()
        self.prepareplot.plotparticle()

        if self.main.rectangleCheckBox.isChecked():
            self.setlocalcombobox()
        
    def phasecombobox(self):

        self.main.particleButton.setChecked(True)
        self.main.field_select_panel[self.main.panelselect-1] = False
        index=self.main.phaseComboBox.currentIndex()
        if self.main.dim == 2:
            self.main.phase_panel[self.main.panelselect-1] = self.main.phase_list1[index]
        else:
            if self.main.sliceplane_panel[self.main.panelselect-1] == 'yx':
                self.main.phase_panel[self.main.panelselect-1] = self.main.phase_list2[index]
            if self.main.sliceplane_panel[self.main.panelselect-1] == 'xz':
                self.main.phase_panel[self.main.panelselect-1] = self.main.phase_list1[index]
            if self.main.sliceplane_panel[self.main.panelselect-1] == 'yz':
                self.main.phase_panel[self.main.panelselect-1] = self.main.phase_list3[index]

        self.collectdata.loadparticle()
        self.prepareplot.plotparticle()

        if self.main.rectangleCheckBox.isChecked():
            self.setlocalcombobox()


    def rectanglecheckbox(self):

        panelselect = self.main.panelselect

        # if the rectangle checkbox is off, remove the rectangle tool
        if not self.main.rectangleCheckBox.isChecked():
            
            [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]
            self.main.canvas.draw_idle()
            self.main.resize[panelselect-1] = 0
            self.main.translate[panelselect-1] = 0
            self.main.rectangle_panel[panelselect-1] = False

            #if self.main.subplot[panelselect]:
            self.main.subplot[panelselect-1].close()

            return

        # if the ractangle checkbox is on, check if the navigation tool is on
        # if the navigation tool is on, turn off the rectangle checkbox
        # to avoid unwanted results.
        if self.main.toolbar.actions()[4].isChecked() or self.main.toolbar.actions()[5].isChecked():
               
            self.main.rectangleCheckBox.setChecked(False)
            self.main.rectangle_panel[panelselect-1] = False
            print('Please turn off the the navagation button to use this function')

            return

        # Create local window panel
        if self.main.field_select_panel[panelselect-1] or \
             self.main.phase_panel[panelselect-1] == ('y','x') or \
             self.main.phase_panel[panelselect-1] == ('x','z') or \
             self.main.phase_panel[panelselect-1] == ('y','z'):

            self.main.rectangle_panel[panelselect-1] = True
            self.main.resize[panelselect-1] = 0
            self.main.translate[panelselect-1] = 0

            size = self.main.geometry()
            mainleft=size.left(); maintop=size.top()
            mainwidth=size.width(); mainheight=size.height()

            self.main.subplot[panelselect-1] = SubWindow(
                        self.main,
                        mainleft,
                        maintop,
                        mainwidth,
                        mainheight)

            self.main.subplot[panelselect-1].show()

            self.setlocalcombobox()

        else:
            print('Local selection is only allowed in the spatial coordinates.')
            print('Please change the menu in the phase combobox.\n')
            self.main.rectangleCheckBox.setChecked(False)


    def setlocalcombobox(self):
        """
        set list in the local combobox
        """

        panelselect = self.main.panelselect

        # field combo-boxes
        self.main.localComboBox.clear() 

        if self.main.field_select_panel[panelselect-1]:
            for i in np.arange(len(self.main.localfield_list)):
                self.main.localComboBox.addItem(self.main.localfield_list[i], i)
            
            localfield = self.main.localfield_panel[panelselect-1]
            index = self.main.localfield_list_indexed[localfield]
            self.main.localComboBox.setCurrentIndex(index)
            
        else:

            localphase = self.main.localphase_panel[panelselect-1]    
            if self.main.dim == 2:
                for i in np.arange(len(self.main.localphase_list1)):
        
                    self.main.localComboBox.addItem(
                        self.main.localphase_list1[i][0]+'-'+self.main.localphase_list1[i][1], i)

                index = self.main.localphase_list1_indexed[localphase]
                self.main.localComboBox.setCurrentIndex(index)

            else:   #3D
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    for i in np.arange(len(self.main.localphase_list2)):
                        
                        self.main.localComboBox.addItem(
                            self.main.localphase_list2[i][0]+'-'+self.main.localphase_list2[i][1], i)

                    index = self.main.localphase_list2_indexed[localphase]
                    self.main.localComboBox.setCurrentIndex(index)

                elif self.main.sliceplane_panel[panelselect-1] == 'xz':
                    for i in np.arange(len(self.main.localphase_list1)):
                        
                        self.main.localComboBox.addItem(
                            self.main.localphase_list1[i][0]+'-'+self.main.localphase_list1[i][1], i)

                    index = self.main.localphase_list1_indexed[localphase]
                    self.main.localComboBox.setCurrentIndex(index)
                    
                elif self.main.sliceplane_panel[panelselect-1] == 'yz':
                    for i in np.arange(len(self.main.localphase_list3)):
                        
                        self.main.localComboBox.addItem(
                            self.main.localphase_list3[i][0]+'-'+self.main.localphase_list3[i][1], i)

                    index = self.main.localphase_list3_indexed[localphase]
                    self.main.localComboBox.setCurrentIndex(index)

    def localcombobox(self):
        """
        response from the siginal emssion in the local combbo box 
        """

        panelselect = self.main.panelselect
        index=self.main.localComboBox.currentIndex()
        if self.main.field_select_panel[panelselect-1]:
            self.main.localfield_panel[self.main.panelselect-1] = self.main.localfield_list[index]
        else:
            if self.main.dim == 2:
                self.main.localphase_panel[self.main.panelselect-1] = self.main.localphase_list1[index]
            else:
                if self.main.sliceplane_panel[self.main.panelselect-1] == 'yx':
                    self.main.localphase_panel[self.main.panelselect-1] = self.main.localphase_list2[index]
                if self.main.sliceplane_panel[self.main.panelselect-1] == 'xz':
                    self.main.localphase_panel[self.main.panelselect-1] = self.main.localphase_list1[index]
                if self.main.sliceplane_panel[self.main.panelselect-1] == 'yz':
                    self.main.localphase_panel[self.main.panelselect-1] = self.main.localphase_list3[index]

        # comment out because this triggers errors
        #if self.main.field_select_panel[panelselect-1]:
        #    PrepareLocalPlot(self.main).plotfield()
        #else:
        #    PrepareLocalPlot(self.main).plotparticle()
            

