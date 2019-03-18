import sys, os, glob

from picviewer.controller.mainwindow import MainWindow 
from picviewer.controller.initialization import Initialization
from picviewer.controller.time_controller import TimeController
from picviewer.controller.space_controller import SpaceController
from picviewer.controller.panel_controller import PanelController
from picviewer.controller.combobox_controller import ComboboxController
from picviewer.controller.slice_controller import SliceController
from picviewer.controller.mouse_controller import MouseController

from picviewer.dataloader.get_datainfo import DataInfo
from picviewer.dataloader.data_collector import DataCollector

from picviewer.dataplotter.prepare_plot import PreparePlot

from picviewer.configuration.config_loadsave import ConfigLoadsave


import threading
import time as tm


from PyQt5 import QtCore, QtGui, QtWidgets

class ControlCenter():
    """
        Main Controller
    """
    def __init__(self):
    
        self.main = MainWindow()
        self.main.show()

        # current folder
        self.main.filepath = os.getcwd()
        # Open data from the current folder
        filelist = glob.glob(self.main.filepath+'/*')
        direct_open = (any('data00' in myfile for myfile in filelist) or \
                      any('plt' in myfile for myfile in filelist) or \
                      any('flds.tot.' in myfile for myfile in filelist))
        if direct_open:
            # Set window title
            self.main.setWindowTitle(os.getcwd())
            
        # Open data from a selected folder, self.main.filepath
        else:
            self.main.filepath = QtWidgets.QFileDialog.getExistingDirectory(
                            None, 'Select a folder:', './',
                            QtWidgets.QFileDialog.ShowDirsOnly)
            # Set window title
            self.main.setWindowTitle(self.main.filepath)

        # ------------------------------------------
        # Initialize classes
        # ------------------------------------------
        # Initialization class (read data and initialize)
        self.initialization = Initialization(self.main)
        # Time Controller class
        self.timecontroller = TimeController(self.main)
        # Space Controller class
        self.spacecontroller = SpaceController(self.main)
        # Panel Controller class
        self.panelcontroller = PanelController(self.main)
        # Create panel buttons
        self.panelcontroller.SetPanelButtons()
        # Combobox Controller class
        self.comboboxcontroller = ComboboxController(self.main)
        self.slicecontroller = SliceController(self.main)
        # get data info class
        self.datainfo = DataInfo()
        # Data collection class
        self.collectdata = DataCollector(self.main)
        # Plot class
        self.prepareplot = PreparePlot(self.main)
        # Mouse controller class
        self.mousecontroller = MouseController(self.main)
        # Configuration load/save class
        self.configloadsave = ConfigLoadsave(self.main)
        

        # time button
        self.main.backwardtimeButton.clicked.connect(self.backwardtimebutton)
        self.main.forwardtimeButton.clicked.connect(self.forwardtimebutton)
        # time slder
        self.main.timeSlider.valueChanged.connect(self.timeslider)
        #self.main.timeSlider.sliderMoved.connect(self.timeslider)

        # space slider
        self.main.x1minSlider.valueChanged.connect(self.x1minslider)
        self.main.x1maxSlider.valueChanged.connect(self.x1maxslider)
        self.main.x2minSlider.valueChanged.connect(self.x2minslider)
        self.main.x2maxSlider.valueChanged.connect(self.x2maxslider)
        # space slider release
        self.main.releaseButton.clicked.connect(self.releasebutton)
        # navigation toolbar home button clicked
        self.main.toolbar.actions()[0].triggered.connect(self.homebutton)

        # field & particle buttons
        #QtCore.QObject.connect(self.main.fieldButton, QtCore.SIGNAL('clicked()'),self.fieldbutton)
        #QtCore.QObject.connect(self.main.particleButton, QtCore.SIGNAL('clicked()'),self.particlebutton)
        self.main.fieldButton.clicked.connect(self.fieldbutton)
        self.main.particleButton.clicked.connect(self.particlebutton)
        # field combobox 
        self.main.fieldsComboBox.activated.connect(self.fieldcombobox)
        # species combobox
        self.main.speciesComboBox.activated.connect(self.speciescombobox)
        # pahse combobox
        self.main.phaseComboBox.activated.connect(self.phasecombobox)
        # local combobox
        self.main.localComboBox.activated.connect(self.localcombobox)

        # slice (xy, xz, yz 2D plane) button in 3D
        #QtCore.QObject.connect(self.main.xyButton, QtCore.SIGNAL('clicked()'),self.slicebutton)
        #QtCore.QObject.connect(self.main.xzButton, QtCore.SIGNAL('clicked()'),self.slicebutton)
        #QtCore.QObject.connect(self.main.yzButton, QtCore.SIGNAL('clicked()'),self.slicebutton)
        self.main.xyButton.clicked.connect(self.slicebutton)
        self.main.xzButton.clicked.connect(self.slicebutton)
        self.main.yzButton.clicked.connect(self.slicebutton)
        self.main.slicevalueSlider.sliderMoved.connect(self.sliceslider)
        self.main.strideSlider.sliderMoved.connect(self.strideslider)
        
       
        # Panel button signal
        for i in range(self.main.nrow):
            for j in range(self.main.ncolumn):
        #        QtCore.QObject.connect(self.main.panelbuttons[(i,j)], QtCore.SIGNAL('clicked()'),self.panelbutton)
                self.main.panelbuttons[(i,j)].clicked.connect(self.panelbutton)
        # Plot button
        self.main.plotButton.clicked.connect(self.plotbutton)
      
        # Aspect ratio checkbox
        self.main.aspectCheckBox.clicked.connect(self.aspectcheckbox)
      
        # Line selection checkbox
        #self.main.lineCheckBox.clicked.connect(self.linecheckbox)
        # Rectangle selection checkbox
        self.main.rectangleCheckBox.clicked.connect(self.rectanglecheckbox)
        
        # Save cofiguration button
        self.main.savepushButton.clicked.connect(self.saveconfig)

        # Load cofiguration button
        self.main.loadpushButton.clicked.connect(self.loadconfig)

         # Quit button
        self.main.quitpushButton.clicked.connect(self.quitpushbutton)

        # animation PushButton
        self.main.animationButton.clicked.connect(self.animationbutton)

        # contrast
        self.main.contrastSlider.valueChanged.connect(self.contrastslider)

        # AMR level
        self.main.amrSpinBox.valueChanged.connect(self.amrspinbox)
        
        # Data load and plot
        self.collectdata.loaddatasync()
        self.prepareplot.plotsync()


    def backwardtimebutton(self):
        self.timecontroller.backwardtime()
     
    def forwardtimebutton(self):
        self.timecontroller.fowardtime()

    def timeslider(self):
        self.timecontroller.timeslider()

    def x1minslider(self):
        self.spacecontroller.x1minslider()

    def x1maxslider(self):
        self.spacecontroller.x1maxslider()

    def x2minslider(self):
        self.spacecontroller.x2minslider()

    def x2maxslider(self):
        self.spacecontroller.x2maxslider()

    def releasebutton(self):
        self.spacecontroller.releasebutton()

    def homebutton(self):
        self.spacecontroller.homebutton()

    def fieldbutton(self):
        self.comboboxcontroller.fieldbutton()

    def amrspinbox(self):
        if self.main.dataformat == 'WarpX':
            amrlevel = self.main.amrSpinBox.value()
            self.main.amrlevel_panel[self.main.panelselect-1] = amrlevel
        else:
            self.amrSpinBox.setValue(0)

    def particlebutton(self):
        self.comboboxcontroller.particlebutton()

    def fieldcombobox(self):
        self.comboboxcontroller.fieldcombobox()

    def speciescombobox(self):
        self.comboboxcontroller.speciescombobox()

    def phasecombobox(self):
        self.comboboxcontroller.phasecombobox()
    
    def localcombobox(self):
        self.comboboxcontroller.localcombobox()
        
    def slicebutton(self):
        self.slicecontroller.slicebutton()

    def sliceslider(self):
        self.slicecontroller.sliceslider()

    def strideslider(self):
        self.slicecontroller.strideslider()

    def contrastslider(self):
        self.slicecontroller.contrastslider()
        
    def panelbutton(self):
        self.panelcontroller.panelbutton()

    def plotbutton(self):
        # re-create panel buttons if asked
        nrow = self.main.rowpanelSpinBox.value()
        ncolumn = self.main.columnpanelSpinBox.value()
        if self.main.nrow != nrow or self.main.ncolumn != ncolumn:
            self.panelcontroller.RecreatePanelButton()
        else:
            if self.main.field_select_panel[self.main.panelselect-1]:
                self.collectdata.loadfield()
                self.prepareplot.plotfield()
            else:
                self.collectdata.loadparticle()
                self.prepareplot.plotparticle()

        # save png image
        if self.main.pngCheckBox.isChecked():
            savedir = '../'
            tstep = self.main.tstep_panel[self.main.panelselect-1]
            if self.main.synctimeBox.isChecked():
                filename = 'multi_plot'
                self.main.figure.savefig(savedir+filename+'%3.3d.png'%(tstep), format='png')

            else:
                filename = self.main.field_panel[self.main.panelselect-1]
                ax = self.main.axes[(self.main.panelselect-1)]
                extent = ax.get_window_extent().transformed(
                        self.main.figure.dpi_scale_trans.inverted())
                self.main.figure.savefig(savedir+filename+'%3.3d.png'%(tstep), format='png',
                        bbox_inches=extent.expanded(1.35, 1.25))

            print('created a file, %s'%(savedir+filename+'%3.3d.png'%(tstep)))


    def aspectcheckbox(self):
        if self.main.aspectCheckBox.isChecked():
            self.main.aspect_panel[self.main.panelselect-1] = 'equal'
        else:
            self.main.aspect_panel[self.main.panelselect-1] = 'auto'

    def linecheckbox(self):
        self.preparelocalplot.linecheckbox()

    def rectanglecheckbox(self):

        self.comboboxcontroller.rectanglecheckbox()
        
    def saveconfig(self):
        self.configloadsave.SaveConfig()
    
    def loadconfig(self):
        self.configloadsave.LoadConfig()


    def quitpushbutton(self):

        sys.exit(0)

    def animationbutton(self):

        self.c_thread=threading.Thread(target=self.myEventListener)
        self.c_thread.start()
    
    # animiation loop begins
    def myEventListener(self):
        tini = self.main.tiniSpinBox.value()
        tmax = self.main.tmaxSpinBox.value()
        step = self.main.stepSpinBox.value()

        if self.main.movieCheckBox.isChecked():
            savedir1 = '../temp_images'
            os.system('mkdir '+savedir1)
            # It is tricky to make a movie or to save an image from one seleted panel. 
            # so, convert to the sync (multi-plot) mode.
            self.main.synctimeBox.setChecked(True)

        if self.main.pngCheckBox.isChecked():
            savedir2 = '../images'
            os.system('mkdir '+savedir2)
            self.main.synctimeBox.setChecked(True)

        s = 0
        for tstep in range(tini,tmax+1,step):
            self.main.time = self.main.taxis[tstep-1]
            # updata time slider
            self.main.tstepLabel.setText("tstep %d" %tstep)
            self.main.timeLabel.setText("%6.1f fs" %self.main.time)
            self.main.timeSlider.setValue(tstep)

            if self.main.synctimeBox.isChecked():
                # sychronize tstep of all the panels               
                self.main.tstep_panel = [tstep for i in range(len(self.main.tstep_panel))]
                self.collectdata.loaddatasync()
                self.prepareplot.plotsync()

                if self.main.movieCheckBox.isChecked():
                    filename = 'multi_plot'
                    self.main.figure.savefig(savedir1+'/'+filename+'%3.3d.png'%(s), format='png')

                if self.main.pngCheckBox.isChecked():
                    filename = 'multi_plot'
                    self.main.figure.savefig(savedir2+'/'+filename+'%3.3d.png'%(s), format='png')

            else:
                self.main.tstep_panel[self.main.panelselect-1] = tstep
                if self.main.field_select_panel[self.main.panelselect-1]:
                    self.collectdata.loadfield()
                    self.prepareplot.plotfield()
                else:
                    self.collectdata.loadparticle()
                    self.prepareplot.plotparticle()

                ####################################################################
                # save an image from a selected panel
                #  ---> This is not working nicely.. so comment them out now.
                ####################################################################
                #if self.main.movieCheckBox.isChecked() or self.main.pngCheckBox.isChecked():
                #    filename = self.main.field_panel[self.main.panelselect-1]
                #    ax = self.main.axes[(self.main.panelselect-1)]
                #    extent = ax.get_window_extent().transformed(
                #            self.main.figure.dpi_scale_trans.inverted())
                #    self.main.figure.savefig(savedir2+'/'+filename+'%3.3d.png'%(s), format='png',
                #            bbox_inches=extent.expanded(1.35, 1.25))
            tm.sleep(0.005)    
            s+=1

        if self.main.movieCheckBox.isChecked():
            # ffmpeg create .mp4 file
            framerate = 4 #int(raw_input("Input a frame rate (#/second): "))
            command = "ffmpeg -framerate %d " %framerate + "-i "+savedir1+"/"+filename+"%03d.png" \
                +" -c:v libx264 -pix_fmt yuv420p -vf scale=1280:-2 ./" + "../"+filename+".mp4"
            os.system(command)
            print('created %s\n'%("../"+filename+".mp4"))

            os.system('rm -rf '+savedir1)


        self.main.movieCheckBox.setChecked(False)
        self.main.pngCheckBox.setChecked(False)