import numpy as np

#from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot

from picviewer.controller.combobox_controller import ComboboxController

class SliceController():
    """
        Slice Control class
        
    """

    def __init__(self,Mainwindow):

        self.main = Mainwindow
 
        # colletc data class
        #self.collectdata = DataCollector(self.main)
        # prepare data class
        self.prepareplot = PreparePlot(self.main)

    def slicebutton(self):

        if self.main.dim == 3:    # only works for 3D

            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            yaxis = self.main.yaxis_dic[tstep-1]
            zaxis = self.main.zaxis_dic[tstep-1]
            
            if self.main.xyButton.isChecked():
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    # if select the same button, return the slice value to the median
                    slicevalue = 25
                    self.main.slicevalueSlider.setValue(slicevalue)
                    self.main.slicevalue_panel[panelselect-1] = slicevalue
                else:
                    self.main.sliceplane_panel[panelselect-1] = 'yx'
                    slicevalue = self.main.slicevalue_panel[panelselect-1]
                    self.main.slicevalueSlider.setValue(slicevalue)
                    # change the space range labels
                    self.ChangeRangeSliderLabels()

                    # change the phase combo-box menus
                    index=self.main.phaseComboBox.currentIndex()
                    self.main.phase_panel[panelselect-1] = self.main.phase_list2[index]
                    self.main.phaseComboBox.clear() 
                    for i in np.arange(len(self.main.phase_list2)):
                        self.main.phaseComboBox.addItem(self.main.phase_list2[i][0]+'-'+self.main.phase_list2[i][1], i)
                    self.main.phaseComboBox.setCurrentIndex(index)
                    
                    if self.main.rectangleCheckBox.isChecked():
                        index=self.main.localComboBox.currentIndex()
                        self.main.localphase_panel[panelselect-1] = self.main.localphase_list2[index]
                        ComboboxController(self.main).setlocalcombobox()

                zvalue = zaxis[0]+(zaxis[-1]-zaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("z=%.2f" %zvalue))
                stride = self.main.strideSlider.value()
                self.main.strideLabel.setText(u'\u0394'+ "z=%.2f" %(stride/50.))

                
            if self.main.xzButton.isChecked():
                if self.main.sliceplane_panel[panelselect-1] == 'xz':
                    # if select the same button, return the slice value to the median
                    slicevalue = 25
                    self.main.slicevalueSlider.setValue(slicevalue)
                    self.main.slicevalue_panel[panelselect-1] = slicevalue
                else:
                    self.main.sliceplane_panel[panelselect-1] = 'xz'
                    slicevalue = self.main.slicevalue_panel[panelselect-1]
                    self.main.slicevalueSlider.setValue(slicevalue)

                    # change the space range labels
                    self.ChangeRangeSliderLabels()

                    # change the phase combo-box menus
                    index=self.main.phaseComboBox.currentIndex()
                    self.main.phase_panel[panelselect-1] = self.main.phase_list1[index]
                    self.main.phaseComboBox.clear() 
                    for i in np.arange(len(self.main.phase_list1)):
                        self.main.phaseComboBox.addItem(self.main.phase_list1[i][0]+'-'+self.main.phase_list1[i][1], i)
                    self.main.phaseComboBox.setCurrentIndex(index)

                    if self.main.rectangleCheckBox.isChecked():
                        index=self.main.localComboBox.currentIndex()
                        self.main.localphase_panel[panelselect-1] = self.main.localphase_list1[index]
                        ComboboxController(self.main).setlocalcombobox()
                    
                yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("y=%.2f" %yvalue))
                stride = self.main.strideSlider.value()
                self.main.strideLabel.setText(u'\u0394'+ "y=%.2f" %(stride/50.))

                
   
            if self.main.yzButton.isChecked():        
                if self.main.sliceplane_panel[panelselect-1] == 'yz':
                    # if select the same button, return the slice value to the median
                    slicevalue = 25
                    self.main.slicevalueSlider.setValue(slicevalue)
                    self.main.slicevalue_panel[panelselect-1] = slicevalue
                else:
                    self.main.sliceplane_panel[panelselect-1] = 'yz'
                    slicevalue = self.main.slicevalue_panel[panelselect-1]
                    self.main.slicevalueSlider.setValue(slicevalue)

                    # change the space range labels
                    self.ChangeRangeSliderLabels()

                    # change the phase combo-box menus
                    index=self.main.phaseComboBox.currentIndex()
                    self.main.phase_panel[panelselect-1] = self.main.phase_list3[index]
                    self.main.phaseComboBox.clear() 
                    for i in np.arange(len(self.main.phase_list3)):
                        self.main.phaseComboBox.addItem(self.main.phase_list3[i][0]+'-'+self.main.phase_list3[i][1], i)
                    self.main.phaseComboBox.setCurrentIndex(index)

                    if self.main.rectangleCheckBox.isChecked():
                        index=self.main.localComboBox.currentIndex()
                        self.main.localphase_panel[panelselect-1] = self.main.localphase_list3[index]
                        ComboboxController(self.main).setlocalcombobox()

                xvalue = xaxis[0]+(xaxis[-1]-xaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("x=%.2f" %xvalue))
                stride = self.main.strideSlider.value()
                self.main.strideLabel.setText(u'\u0394'+ "x=%.2f" %(stride/50.))

                
        else:
            self.main.xzButton.setChecked(True)

        if self.main.dim == 3:

            if self.main.field_select_panel[self.main.panelselect-1]:
                #self.collectdata.loadfield()
                self.prepareplot.plotfield()
            else:
                #self.collectdata.loadparticle()
                self.prepareplot.plotparticle()


            if self.main.rectangleCheckBox.isChecked():
            
                [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]
                self.main.canvas.draw_idle()
                self.main.resize[:] = 0
                self.main.translate[:] = False
                #self.main.rectangle_panel[panelselect-1] = False



    def sliceslider(self):
        """
        Slider for the 3rd axis

        """
        if self.main.dim == 3:

            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            yaxis = self.main.yaxis_dic[tstep-1]
            zaxis = self.main.zaxis_dic[tstep-1]

            slicevalue = self.main.slicevalueSlider.value()
            self.main.slicevalue_panel[panelselect-1] = slicevalue
            if self.main.sliceplane_panel[panelselect-1] == 'yx':
                zvalue = zaxis[0]+(zaxis[-1]-zaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("z=%.2f" %zvalue))
            if self.main.sliceplane_panel[panelselect-1] == 'xz':
                yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("y=%.2f" %yvalue))
            if self.main.sliceplane_panel[panelselect-1] == 'yz':
                xvalue = xaxis[0]+(xaxis[-1]-xaxis[0])*slicevalue/50.
                self.main.slicevalueLabel.setText(str("x=%.2f" %xvalue))

            if self.main.field_select_panel[panelselect-1]:
                #self.collectdata.loadfield()
                self.prepareplot.plotfield()
            else:
                #self.collectdata.loadparticle()
                self.prepareplot.plotparticle()
                
        else:
            self.main.slicevalueSlider.setValue(25)

    def strideslider(self):
        """
        Stride in the 3rd axis for particle selection

        """
        if self.main.dim == 3:
            if self.main.particleButton.isChecked():
                panelselect = self.main.panelselect
                stride = self.main.strideSlider.value()
                self.main.stride_panel[panelselect-1] = stride
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    self.main.strideLabel.setText(u'\u0394'+ "z=%.2f" %(stride/50.))
                if self.main.sliceplane_panel[panelselect-1] == 'xz':
                    self.main.strideLabel.setText(u'\u0394'+ "y=%.2f" %(stride/50.))
                if self.main.sliceplane_panel[panelselect-1] == 'yz':
                    self.main.strideLabel.setText(u'\u0394'+ "x=%.2f" %(stride/50.))

                #self.collectdata.loadparticle()
                self.prepareplot.plotparticle()
        else:
            self.main.strideSlider.setValue(25)



    def ChangeRangeSliderLabels(self):
        """
        Change the space range labels

        """

        panelselect = self.main.panelselect
        tstep = self.main.tstep_panel[panelselect-1]
        xaxis = self.main.xaxis_dic[tstep-1]
        yaxis = self.main.yaxis_dic[tstep-1]
        zaxis = self.main.zaxis_dic[tstep-1]

        if self.main.dim == 3:
            if self.main.sliceplane_panel[panelselect-1] == 'yx':
                self.main.x1min.setText("xmin")
                self.main.x1max.setText("xmax")
                self.main.x2min.setText("ymin")
                self.main.x2max.setText("ymax")
                xminloc = self.main.xminloc_panel[panelselect-1]
                xmaxloc = self.main.xmaxloc_panel[panelselect-1]
                yminloc = self.main.yminloc_panel[panelselect-1]
                ymaxloc = self.main.ymaxloc_panel[panelselect-1]
                self.main.x1minSlider.setValue(xminloc)
                self.main.x1maxSlider.setValue(xmaxloc)
                self.main.x2minSlider.setValue(yminloc)
                self.main.x2maxSlider.setValue(ymaxloc)
                xmin=xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                xmax=xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
                ymin=yaxis[0]+(yaxis[-1]-yaxis[0])*yminloc/100.
                ymax=yaxis[0]+(yaxis[-1]-yaxis[0])*ymaxloc/100.
                self.main.x1minLabel.setText(str("%.1f" %xmin))
                self.main.x1maxLabel.setText(str("%.1f" %xmax))
                self.main.x2minLabel.setText(str("%.1f" %ymin))
                self.main.x2maxLabel.setText(str("%.1f" %ymax))
                

            if self.main.sliceplane_panel[panelselect-1] == 'xz':
                self.main.x1min.setText("zmin")
                self.main.x1max.setText("zmax")
                self.main.x2min.setText("xmin")
                self.main.x2max.setText("xmax")
                xminloc = self.main.xminloc_panel[panelselect-1]
                xmaxloc = self.main.xmaxloc_panel[panelselect-1]
                zminloc = self.main.zminloc_panel[panelselect-1]
                zmaxloc = self.main.zmaxloc_panel[panelselect-1]
                self.main.x1minSlider.setValue(zminloc)
                self.main.x1maxSlider.setValue(zmaxloc)
                self.main.x2minSlider.setValue(xminloc)
                self.main.x2maxSlider.setValue(xmaxloc)
                xmin=xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                xmax=xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
                zmin=zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100. 
                zmax=zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100. 
                self.main.x1minLabel.setText(str("%.1f" %zmin))
                self.main.x1maxLabel.setText(str("%.1f" %zmax))
                self.main.x2minLabel.setText(str("%.1f" %xmin))
                self.main.x2maxLabel.setText(str("%.1f" %xmax))

            if self.main.sliceplane_panel[panelselect-1] == 'yz':
                self.main.x1min.setText("zmin")
                self.main.x1max.setText("zmax")
                self.main.x2min.setText("ymin")
                self.main.x2max.setText("ymax")
                yminloc = self.main.yminloc_panel[panelselect-1]
                ymaxloc = self.main.ymaxloc_panel[panelselect-1]
                zminloc = self.main.zminloc_panel[panelselect-1]
                zmaxloc = self.main.zmaxloc_panel[panelselect-1]
                self.main.x1minSlider.setValue(zminloc)
                self.main.x1maxSlider.setValue(zmaxloc)
                self.main.x2minSlider.setValue(yminloc)
                self.main.x2maxSlider.setValue(ymaxloc)
                ymin=yaxis[0]+(yaxis[-1]-yaxis[0])*yminloc/100. 
                ymax=yaxis[0]+(yaxis[-1]-yaxis[0])*ymaxloc/100.
                zmin=zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100. 
                zmax=zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100. 
                self.main.x1minLabel.setText(str("%.1f" %zmin))
                self.main.x1maxLabel.setText(str("%.1f" %zmax))
                self.main.x2minLabel.setText(str("%.1f" %ymin))
                self.main.x2maxLabel.setText(str("%.1f" %ymax))

        else:
                xminloc = self.main.xminloc_panel[panelselect-1]
                xmaxloc = self.main.xmaxloc_panel[panelselect-1]
                zminloc = self.main.zminloc_panel[panelselect-1]
                zmaxloc = self.main.zmaxloc_panel[panelselect-1]
                self.main.x1minSlider.setValue(zminloc)
                self.main.x1maxSlider.setValue(zmaxloc)
                self.main.x2minSlider.setValue(xminloc)
                self.main.x2maxSlider.setValue(xmaxloc)
                xmin=xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                xmax=xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
                zmin=zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100. 
                zmax=zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100. 
                self.main.x1minLabel.setText(str("%.1f" %zmin))
                self.main.x1maxLabel.setText(str("%.1f" %zmax))
                self.main.x2minLabel.setText(str("%.1f" %xmin))
                self.main.x2maxLabel.setText(str("%.1f" %xmax))


    def contrastslider(self):

        panelselect = self.main.panelselect
        contrast = self.main.contrastSlider.value()
        self.main.contrast_panel[panelselect-1] = contrast
        self.main.contrastLabel.setText(str("%d%%" %contrast))

        if self.main.field_select_panel[panelselect-1]:
            self.prepareplot.plotfield()
        #else:
        #    self.prepareplot.plotparticle()