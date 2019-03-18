import csv

from PyQt5 import QtWidgets


from picviewer.controller.panel_controller import PanelController
from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot


class ConfigLoadsave():

    def __init__(self,Mainwindow):

        self.main = Mainwindow

        self.panelcontroller = PanelController(self.main)

        # Data collect class
        self.collectdata = DataCollector(self.main)
        # Plot class
        self.prepareplot = PreparePlot(self.main)

    def SaveConfig(self):

        filename, filter = QtWidgets.QFileDialog.getSaveFileName(self.main, 'Save file', 'config.txt', filter='*.txt')

        if not filename:
            return
        
        f = open(filename,'w')

        f.write('filepath, %s \n'%(self.main.filepath))
        f.write('nrow, %d \n'%(self.main.nrow))
        f.write('ncolumn, %d \n'%(self.main.ncolumn))
        for l in range(self.main.nrow*self.main.ncolumn):
            f.write('tstep_panel, %d, %d \n'%(l, self.main.tstep_panel[l]))
            f.write('field_select_panel, %d, %r \n'%(l, self.main.field_select_panel[l]))
            f.write('field_panel, %d, %s \n'%(l, self.main.field_panel[l]))
            f.write('species_panel, %d, %s \n'%(l, self.main.species_panel[l]))
            f.write('phase_panel, %d, %s, %s \n'%(l, 
                        self.main.phase_panel[l][0], self.main.phase_panel[l][1]))
            f.write('line_panel, %d, %r \n'%(l, self.main.line_panel[l]))
            f.write('rectangle_panel, %d, %r \n'%(l, self.main.rectangle_panel[l]))
            f.write('aspect_panel, %d, %s \n'%(l, self.main.aspect_panel[l]))
            f.write('xminloc_panel, %d, %d \n'%(l, self.main.xminloc_panel[l]))
            f.write('xmaxloc_panel, %d, %d \n'%(l, self.main.xmaxloc_panel[l]))
            f.write('zminloc_panel, %d, %d \n'%(l, self.main.zminloc_panel[l]))
            f.write('zmaxloc_panel, %d, %d \n'%(l, self.main.zmaxloc_panel[l]))
            f.write('contrast_panel, %d, %d \n'%(l, self.main.contrast_panel[l]))
            f.write('amrlevel_panel, %d, %d \n'%(l, self.main.amrlevel_panel[l]))
            if self.main.dim == 3:
                f.write('sliceplane_panel, %d, %s \n'%(l, self.main.sliceplane_panel[l]))
                f.write('slicevalue_panel, %d, %d \n'%(l, self.main.slicevalue_panel[l]))
                f.write('stride_panel, %d, %d \n'%(l, self.main.stride_panel[l]))
                f.write('yminloc_panel, %d, %d \n'%(l, self.main.yminloc_panel[l]))
                f.write('ymaxloc_panel, %d, %d \n'%(l, self.main.ymaxloc_panel[l]))
         

        print('configuration file saved')
        f.close()

    def LoadConfig(self):


        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.main, caption='Open file', directory='.', filter='*.txt')
        
        if not filename:
            return

        savedparam = {}
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if len(row) == 2:
                    savedparam[row[0].strip()] = row[1].strip()
                # below is for the panel parmaters
                if len(row) == 3:
                    savedparam[(row[0].strip(),row[1].strip())] = row[2].strip()
                elif len(row) == 4:
                    savedparam[(row[0].strip(),row[1].strip())] = (row[2].strip(),row[3].strip())
        
        # Load file path
        self.main.filepath = savedparam['filepath']
        # Set Title
        self.main.setWindowTitle(self.main.filepath)
        # Load the numbers of rows and columns 
        self.main.nrow = int(savedparam['nrow'])
        self.main.ncolumn = int(savedparam['ncolumn'])
        # Set the row and column spin box
        self.main.rowpanelSpinBox.setValue(self.main.nrow)
        self.main.columnpanelSpinBox.setValue(self.main.ncolumn)
        
        self.main.tstep_panel = []
        self.main.field_select_panel = []
        self.main.field_panel = []
        self.main.species_panel = []
        self.main.phase_panel = []
        self.main.line_panel = []
        self.main.rectangle_panel = []
        self.main.aspect_panel = []
        self.main.xminloc_panel = []
        self.main.xmaxloc_panel = []
        self.main.zminloc_panel = []
        self.main.zmaxloc_panel = []
        self.main.contrast_panel = []
        self.main.amrlevel_panel = []
        
        if self.main.dim == 3:
            self.main.sliceplane_panel = []
            self.main.slicevalue_panel = []
            self.main.stride_panel = []
            self.main.yminloc_panel = []
            self.main.ymaxloc_panel = []

        for l in range(self.main.nrow*self.main.ncolumn):
            
            self.main.tstep_panel.append(int(savedparam[('tstep_panel',str(l))]))
            self.main.field_select_panel.append(eval(savedparam[('field_select_panel',str(l))]))
            self.main.field_panel.append(savedparam[('field_panel',str(l))])
            self.main.species_panel.append(savedparam[('species_panel',str(l))])
            self.main.phase_panel.append(savedparam[('phase_panel', str(l))])
            self.main.line_panel.append(eval(savedparam[('line_panel', str(l))]))
            self.main.rectangle_panel.append(eval(savedparam[('rectangle_panel', str(l))]))
            self.main.aspect_panel.append(savedparam[('aspect_panel', str(l))])
            self.main.xminloc_panel.append(int(savedparam[('xminloc_panel', str(l))]))
            self.main.xmaxloc_panel.append(int(savedparam[('xmaxloc_panel', str(l))]))
            self.main.zminloc_panel.append(int(savedparam[('zminloc_panel', str(l))]))
            self.main.zmaxloc_panel.append(int(savedparam[('zmaxloc_panel', str(l))]))
            self.main.contrast_panel.append(int(savedparam[('contrast_panel', str(l))]))
            self.main.amrlevel_panel.append(int(savedparam[('amrlevel_panel', str(l))]))
            if self.main.dim == 3:
                self.main.sliceplane_panel.append(savedparam[('sliceplane_panel', str(l))])
                self.main.slicevalue_panel.append(int(savedparam[('slicevalue_panel', str(l))]))
                self.main.stride_panel.append(int(savedparam[('stride_panel', str(l))]))
                self.main.yminloc_panel.append(int(savedparam[('yminloc_panel', str(l))]))
                self.main.ymaxloc_panel.append(int(savedparam[('ymaxloc_panel', str(l))]))   

        self.collectdata.loaddatasync()
        self.prepareplot.plotsync()

        # Re-create the panel buttons
        self.main.panellayout.deleteLater()
        # Update the panel buttons
        self.panelcontroller.SetPanelButtons()

