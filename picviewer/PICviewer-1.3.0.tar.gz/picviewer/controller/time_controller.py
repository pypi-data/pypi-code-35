from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot

from picviewer.controller.slice_controller import SliceController

class TimeController():
    """
        time control class
        
        Returns:
            None
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow
        
        #self.datainfo = DataInfo()

        # Data collect class
        self.collectdata = DataCollector(self.main)
        # Plot class
        self.prepareplot = PreparePlot(self.main)

        self.slicecontroller = SliceController(self.main)

    def backwardtime(self):
        
        panelselect = self.main.panelselect
        tstride = self.main.stepSpinBox.value()
        tstep = self.main.timeSlider.value()
        tstep = tstep - tstride
        if tstep < 1:
            tstep = tstep + tstride
        else:
            self.main.tstepLabel.setText("tstep %d" %tstep)
            time = self.main.taxis[tstep-1]
            self.main.timeLabel.setText("%6.1f fs" %time )
            self.main.timeSlider.setValue(tstep)

        if not self.main.synctimeBox.isChecked():
            self.main.tstep_panel[panelselect-1] = tstep
        else:
            self.main.tstep_panel = [tstep for ind in range(len(self.main.tstep_panel))]
                
        self.slicecontroller.ChangeRangeSliderLabels()

        if self.main.synctimeBox.isChecked():
            self.collectdata.loaddatasync()
            self.prepareplot.plotsync()
        else:
            if self.main.field_select_panel[panelselect-1]:
                self.collectdata.loadfield()
                self.prepareplot.plotfield()
            else:
                self.collectdata.loadparticle()
                self.prepareplot.plotparticle()

    def fowardtime(self):
        
        panelselect = self.main.panelselect
        tstride = self.main.stepSpinBox.value()
        tstep = self.main.timeSlider.value()
        tstep = tstep + tstride
        if tstep > len(self.main.taxis):
            tstep = tstep - tstride
        else:
            self.main.tstepLabel.setText("tstep %d" %tstep)
            time = self.main.taxis[tstep-1]
            self.main.timeLabel.setText("%6.1f fs" %time)
            self.main.timeSlider.setValue(tstep)

        if not self.main.synctimeBox.isChecked():
            self.main.tstep_panel[panelselect-1] = tstep
        else:
            self.main.tstep_panel = [tstep for ind in range(len(self.main.tstep_panel))]

        self.slicecontroller.ChangeRangeSliderLabels()

        if self.main.synctimeBox.isChecked():
            self.collectdata.loaddatasync()
            self.prepareplot.plotsync()
        else:
            if self.main.field_select_panel[panelselect-1]:
                self.collectdata.loadfield()
                self.prepareplot.plotfield()
            else:
                self.collectdata.loadparticle()
                self.prepareplot.plotparticle()


    def timeslider(self):

        tstep = self.main.timeSlider.value()
        self.main.tstepLabel.setText("tstep %d" %tstep)
        self.main.timeLabel.setText("%6.1f fs" %self.main.taxis[tstep-1])

        if not self.main.synctimeBox.isChecked():
            self.main.tstep_panel[self.main.panelselect-1] = tstep
        else:
            self.main.tstep_panel = [tstep for ind in range(len(self.main.tstep_panel))]

        self.slicecontroller.ChangeRangeSliderLabels()

        