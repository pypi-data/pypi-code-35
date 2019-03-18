from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot


class SpaceController():
    """
        space control class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow

        # Data collect class
        self.collectdata = DataCollector(self.main)
        # Plot class
        self.prepareplot = PreparePlot(self.main)
        
    def x1minslider(self):

        if not self.main.home:

            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            zaxis = self.main.zaxis_dic[tstep-1]

            x1minloc = self.main.x1minSlider.value()
            x1maxloc = self.main.x1maxSlider.value()
            if x1minloc > x1maxloc: 
                x1minloc = x1maxloc - 2
                self.main.x1minSlider.setValue(x1minloc)
            if self.main.dim == 3:
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    xmin = xaxis[0]+(xaxis[-1]-xaxis[0])*x1minloc/100. 
                    self.main.x1minLabel.setText(str("%.1f" %xmin))
                    self.main.xminloc_panel[panelselect-1] = x1minloc
                if self.main.sliceplane_panel[panelselect-1] == 'xz':
                    zmin = zaxis[0]+(zaxis[-1]-zaxis[0])*x1minloc/100.
                    self.main.x1minLabel.setText(str("%.1f" %zmin))
                    self.main.zminloc_panel[panelselect-1] = x1minloc
                if self.main.sliceplane_panel[panelselect-1] == 'yz':
                    zmin = zaxis[0]+(zaxis[-1]-zaxis[0])*x1minloc/100. 
                    self.main.x1minLabel.setText(str("%.1f" %zmin))
                    self.main.zminloc_panel[panelselect-1] = x1minloc
            else:
                zmin = zaxis[0]+(zaxis[-1]-zaxis[0])*(x1minloc)/100.
                self.main.x1minLabel.setText(str("%.1f" %zmin))
                self.main.zminloc_panel[panelselect-1] = x1minloc

        else:

            for l in range(self.main.nrow*self.main.ncolumn):
                tstep = self.main.tstep_panel[l]
                xaxis = self.main.xaxis_dic[tstep-1]
                zaxis = self.main.zaxis_dic[tstep-1]
                if self.main.dim == 3:
                    if self.main.sliceplane_panel[l] == 'yx':
                        self.main.x1minLabel.setText(str("%.1f" %xaxis[0]))
                        self.main.xminloc_panel[l] = 0
                    if self.main.sliceplane_panel[l] == 'xz':
                        self.main.x1minLabel.setText(str("%.1f" %zaxis[0]))
                        self.main.zminloc_panel[l] = 0
                    if self.main.sliceplane_panel[l] == 'yz':
                        self.main.x1minLabel.setText(str("%.1f" %zaxis[0]))
                        self.main.zminloc_panel[l] = 0
                else:
                    self.main.x1minLabel.setText(str("%.1f" %zaxis[0]))
                    self.main.zminloc_panel[l] = 0


    
    def x1maxslider(self):

        if not self.main.home:

            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            zaxis = self.main.zaxis_dic[tstep-1]

            x1minloc = self.main.x1minSlider.value()
            x1maxloc = self.main.x1maxSlider.value()
            if x1maxloc < x1minloc: 
                x1maxloc = x1minloc + 2
                self.main.x1maxSlider.setValue(x1maxloc)
            if self.main.dim == 3:
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    xmax = xaxis[0]+(xaxis[-1]-xaxis[0])*x1maxloc/100. 
                    self.main.x1maxLabel.setText(str("%.1f" %xmax))
                    self.main.xmaxloc_panel[panelselect-1] = x1maxloc
                if self.main.sliceplane_panel[panelselect-1] == 'xz':
                    zmax = zaxis[0]+(zaxis[-1]-zaxis[0])*x1maxloc/100.
                    self.main.x1maxLabel.setText(str("%.1f" %zmax))
                    self.main.zmaxloc_panel[panelselect-1] = x1maxloc
                if self.main.sliceplane_panel[panelselect-1] == 'yz':
                    zmax = zaxis[0]+(zaxis[-1]-zaxis[0])*x1maxloc/100. 
                    self.main.x1maxLabel.setText(str("%.1f" %zmax))
                    self.main.zmaxloc_panel[panelselect-1] = x1maxloc
            else:
                zmax = zaxis[0]+(zaxis[-1]-zaxis[0])*(x1maxloc)/100.
                self.main.x1maxLabel.setText(str("%.1f" %zmax))
                self.main.zmaxloc_panel[panelselect-1] = x1maxloc

        else:

            for l in range(self.main.nrow*self.main.ncolumn):
                tstep = self.main.tstep_panel[l]
                xaxis = self.main.xaxis_dic[tstep-1]
                zaxis = self.main.zaxis_dic[tstep-1]
                if self.main.dim == 3:
                    if self.main.sliceplane_panel[l] == 'yx':
                        self.main.x1maxLabel.setText(str("%.1f" %xaxis[-1]))
                        self.main.xmaxloc_panel[l] = 100
                    if self.main.sliceplane_panel[l] == 'xz':
                        self.main.x1maxLabel.setText(str("%.1f" %zaxis[-1]))
                        self.main.zmaxloc_panel[l] = 100
                    if self.main.sliceplane_panel[l] == 'yz':
                        self.main.x1maxLabel.setText(str("%.1f" %zaxis[-1]))
                        self.main.zmaxloc_panel[l] = 100
                else:
                    self.main.x1maxLabel.setText(str("%.1f" %zaxis[-1]))
                    self.main.zmaxloc_panel[l] = 100


    def x2minslider(self):

        if not self.main.home:

            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            yaxis = self.main.yaxis_dic[tstep-1]

            x2minloc = self.main.x2minSlider.value()
            x2maxloc = self.main.x2maxSlider.value()
            if x2minloc > x2maxloc: 
                x2minloc = x2maxloc - 2
                self.main.x2minSlider.setValue(x2minloc)
            if self.main.dim == 3:
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    ymin = yaxis[0]+(yaxis[-1]-yaxis[0])*x2minloc/100. 
                    self.main.x2minLabel.setText(str("%.1f" %ymin))
                    self.main.yminloc_panel[panelselect-1] = x2minloc
                if self.main.sliceplane_panel[panelselect-1] == 'xz':
                    xmin = xaxis[0]+(xaxis[-1]-xaxis[0])*x2minloc/100.
                    self.main.x2minLabel.setText(str("%.1f" %xmin))
                    self.main.xminloc_panel[panelselect-1] = x2minloc
                if self.main.sliceplane_panel[panelselect-1] == 'yz':
                    ymin = yaxis[0]+(yaxis[-1]-yaxis[0])*x2minloc/100. 
                    self.main.x2minLabel.setText(str("%.1f" %ymin))
                    self.main.yminloc_panel[panelselect-1] = x2minloc
            else:
                xmin = xaxis[0]+(xaxis[-1]-xaxis[0])*(x2minloc)/100.
                self.main.x2minLabel.setText(str("%.1f" %xmin))
                self.main.xminloc_panel[panelselect-1] = x2minloc

        else:

            for l in range(self.main.nrow*self.main.ncolumn):
                tstep = self.main.tstep_panel[l]
                xaxis = self.main.xaxis_dic[tstep-1]
                yaxis = self.main.yaxis_dic[tstep-1]
                if self.main.dim == 3:
                    if self.main.sliceplane_panel[l] == 'yx':
                        self.main.x2minLabel.setText(str("%.1f" %yaxis[0]))
                        self.main.yminloc_panel[l] = 0
                    if self.main.sliceplane_panel[l] == 'xz':
                        self.main.x2minLabel.setText(str("%.1f" %xaxis[0]))
                        self.main.xminloc_panel[l] = 0
                    if self.main.sliceplane_panel[l] == 'yz':
                        self.main.x2minLabel.setText(str("%.1f" %yaxis[0]))
                        self.main.yminloc_panel[l] = 0
                else:
                    self.main.x2minLabel.setText(str("%.1f" %xaxis[0]))
                    self.main.xminloc_panel[l] = 0


    
    def x2maxslider(self):

        if not self.main.home:

            panelselect = self.main.panelselect
            tstep = self.main.tstep_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            yaxis = self.main.yaxis_dic[tstep-1]

            x2minloc = self.main.x2minSlider.value()
            x2maxloc = self.main.x2maxSlider.value()
            if x2maxloc < x2minloc: 
                x2maxloc = x2minloc + 2
                self.main.x2maxSlider.setValue(x2maxloc)
            if self.main.dim == 3:
                if self.main.sliceplane_panel[panelselect-1] == 'yx':
                    ymax = yaxis[0]+(yaxis[-1]-yaxis[0])*x2maxloc/100. 
                    self.main.x2maxLabel.setText(str("%.1f" %ymax))
                    self.main.ymaxloc_panel[panelselect-1] = x2maxloc
                if self.main.sliceplane_panel[panelselect-1] == 'xz':
                    xmax = xaxis[0]+(xaxis[-1]-xaxis[0])*x2maxloc/100. 
                    self.main.x2maxLabel.setText(str("%.1f" %xmax))
                    self.main.xmaxloc_panel[panelselect-1] = x2maxloc
                if self.main.sliceplane_panel[panelselect-1] == 'yz':
                    ymax = yaxis[0]+(yaxis[-1]-yaxis[0])*x2maxloc/100. 
                    self.main.x2maxLabel.setText(str("%.1f" %ymax))
                    self.main.ymaxloc_panel[panelselect-1] = x2maxloc
            else:
                xmax = xaxis[0]+(xaxis[-1]-xaxis[0])*x2maxloc/100. 
                self.main.x2maxLabel.setText(str("%.1f" %xmax))
                self.main.xmaxloc_panel[panelselect-1] = x2maxloc

        else:

            for l in range(self.main.nrow*self.main.ncolumn):
                tstep = self.main.tstep_panel[l]
                xaxis = self.main.xaxis_dic[tstep-1]
                yaxis = self.main.yaxis_dic[tstep-1]
                if self.main.dim == 3:
                    if self.main.sliceplane_panel[l] == 'yx':
                        self.main.x2maxLabel.setText(str("%.1f" %yaxis[-1]))
                        self.main.ymaxloc_panel[l] = 100
                    if self.main.sliceplane_panel[l] == 'xz':
                        self.main.x2maxLabel.setText(str("%.1f" %xaxis[-1]))
                        self.main.xmaxloc_panel[l] = 100
                    if self.main.sliceplane_panel[l] == 'yz':
                        self.main.x2maxLabel.setText(str("%.1f" %yaxis[-1]))
                        self.main.ymaxloc_panel[l] = 100
                else:
                    self.main.x2maxLabel.setText(str("%.1f" %xaxis[-1]))
                    self.main.xmaxloc_panel[l] = 100

        

    def releasebutton(self):
        """
        Return to the original space range

        """

        panelselect = self.main.panelselect

        self.main.x1minSlider.setValue(0)
        self.main.x1maxSlider.setValue(100)
        self.main.x2minSlider.setValue(0)
        self.main.x2maxSlider.setValue(100)

        if self.main.field_select_panel[panelselect-1]:
            self.collectdata.loadfield()
            self.prepareplot.plotfield()
        else:
            self.collectdata.loadparticle()
            self.prepareplot.plotparticle()

    def homebutton(self):
        """
        Return to the original space range in all panels

        """

        self.main.home = True

        self.main.x1minSlider.setValue(0)
        self.main.x1maxSlider.setValue(100)
        self.main.x2minSlider.setValue(0)
        self.main.x2maxSlider.setValue(100)

        self.collectdata.loaddatasync()
        self.prepareplot.plotsync()

        self.main.home = False
        