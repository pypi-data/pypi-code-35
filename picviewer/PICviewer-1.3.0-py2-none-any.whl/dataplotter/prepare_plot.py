import numpy as np
from picviewer.dataplotter.makeplot import MakePlot

from picviewer.dataplotter.cic_histogram import particle_energy


class PreparePlot():
    """
        Plot Data class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow

        self.makeplot = MakePlot(self.main)
        
    def plotsync(self):

        if self.main.dim == 2:
            # self.axes: return value from each subpanel axis
            # self.cbars: return value from each subpanel colorbar
            self.main.axes, self.main.cbars = self.makeplot.makeplotsync2D()

        else:   # 3D

            loc_container = self.getLocalparticleLoc()
            self.main.axes, self.main.cbars = self.makeplot.makeplotsync3D(
                    loc_container)
 
        self.main.canvas.draw()


    def plotfield(self):

        x1min, x1max, \
        x2min, x2max, \
        iloc1, iloc2, \
        jloc1, jloc2, \
        kloc1, kloc2 = self.getSpaceRanges()

        panelselect = self.main.panelselect

        if self.main.dim == 2:

            self.main.axes[panelselect-1], self.main.cbars[panelselect-1] = self.makeplot.plotfield2D(
                            x1min,x1max,x2min,x2max,
                            iloc1,iloc2,jloc1,jloc2)

        else:   # 3D
            self.main.axes[panelselect-1], self.main.cbars[panelselect-1]=self.makeplot.plotfield3D(
                            x1min,x1max,x2min,x2max,
                            iloc1,iloc2,jloc1,jloc2,
                            kloc1,kloc2)

        self.main.canvas.draw()

    def plotparticle(self):

        panelselect = self.main.panelselect
        
        # get space range of the current selected panel
        x1min, x1max, \
        x2min, x2max, \
        dummy, dummy, \
        dummy, dummy, \
        dummy, dummy = self.getSpaceRanges()

        if self.main.dim == 2:
            local = []
            self.main.axes[panelselect-1], self.main.cbars[panelselect-1] = self.makeplot.plotparticle(
                            x1min,x1max,
                            x2min,x2max,
                            local)

        else:

            tstep = self.main.tstep_panel[panelselect-1]
            species = self.main.species_panel[panelselect-1]
            xaxis = self.main.xaxis_dic[tstep-1]
            yaxis = self.main.yaxis_dic[tstep-1]
            zaxis = self.main.zaxis_dic[tstep-1]

            sliceplane = self.main.sliceplane_panel[panelselect-1]
            slicevalue = self.main.slicevalue_panel[panelselect-1]
            stride = self.main.stride_panel[panelselect-1]

            if sliceplane == 'yx':
                zvalue = zaxis[0]+(zaxis[-1]-zaxis[0])*(slicevalue/50.)
                width = (zaxis[-1]-zaxis[0])*(stride/50.)
                local = np.where((self.main.pdata_container[(species,'z',tstep)] > zvalue-.5*width) & \
                       (self.main.pdata_container[(species,'z',tstep)] < zvalue+.5*width))[0]
                
            if sliceplane == 'xz':
                yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*(slicevalue/50.)
                width = (yaxis[-1]-yaxis[0])*(stride/50.)
                local = np.where((self.main.pdata_container[(species,'y',tstep)] > yvalue-.5*width) & \
                       (self.main.pdata_container[(species,'y',tstep)] < yvalue+.5*width))[0]

            if sliceplane == 'yz':
                xvalue = xaxis[0]+(xaxis[-1]-xaxis[0])*(slicevalue/50.)
                width = (xaxis[-1]-xaxis[0])*(stride/50.)
                local = np.where((self.main.pdata_container[(species,'x',tstep)] > xvalue-.5*width) & \
                       (self.main.pdata_container[(species,'x',tstep)] < xvalue+.5*width))[0]

            self.main.axes[panelselect-1], self.main.cbars[self.main.panelselect-1] = self.makeplot.plotparticle(
                            x1min,x1max,
                            x2min,x2max,
                            local)

        self.main.canvas.draw()

    def getLocalparticleLoc(self):
        """
        Select particle indices located within the particle stride of the 3rd axis
        """
        loc_container = {}

        stride = self.main.strideSlider.value()

        for l in range(self.main.nrow*self.main.ncolumn):

            if not self.main.field_select_panel[l]:

                tstep = self.main.tstep_panel[l]
                species = self.main.species_panel[l]
                xaxis = self.main.xaxis_dic[tstep-1]
                yaxis = self.main.yaxis_dic[tstep-1]
                zaxis = self.main.zaxis_dic[tstep-1]
                slicevalue = self.main.slicevalue_panel[l]
                
                if self.main.sliceplane_panel[l] == 'yx':
                    zvalue = zaxis[0]+(zaxis[-1]-zaxis[0])*(slicevalue/50.)
                    width = (zaxis[-1]-zaxis[0])*(stride/50.)
                    loc = np.where((self.main.pdata_container[(species,'z',tstep)] > zvalue-.5*width) & \
                        (self.main.pdata_container[(species,'z',tstep)] < zvalue+.5*width))[0]

                if self.main.sliceplane_panel[l] == 'xz':
                    yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*(slicevalue/50.)
                    width = (yaxis[-1]-yaxis[0])*(stride/50.)
                    loc = np.where((self.main.pdata_container[(species,'y',tstep)] > yvalue-.5*width) & \
                        (self.main.pdata_container[(species,'y',tstep)] < yvalue+.5*width))[0]

                if self.main.sliceplane_panel[l] == 'yz':
                    xvalue = xaxis[0]+(xaxis[-1]-xaxis[0])*(slicevalue/50.)
                    width = (xaxis[-1]-xaxis[0])*(stride/50.)
                    loc = np.where((self.main.pdata_container[(species,'x',tstep)] > xvalue-.5*width) & \
                        (self.main.pdata_container[(species,'x',tstep)] < xvalue+.5*width))[0]

                loc_container[l] = loc

        return loc_container

    def getSpaceRanges(self):
        """
        Get space range values

        """
        panelselect = self.main.panelselect
        tstep = self.main.tstep_panel[panelselect-1]
        xaxis = self.main.xaxis_dic[tstep-1]
        yaxis = self.main.yaxis_dic[tstep-1]
        zaxis = self.main.zaxis_dic[tstep-1]
        amrlevel = self.main.amrlevel_panel[panelselect-1]
        dim_factor = 2**amrlevel

        if self.main.dim == 2:
            # xminloc, xmaxloc, ... are values in [0,99]
            xminloc = self.main.xminloc_panel[panelselect-1]
            xmaxloc = self.main.xmaxloc_panel[panelselect-1]
            zminloc = self.main.zminloc_panel[panelselect-1]
            zmaxloc = self.main.zmaxloc_panel[panelselect-1]
            # x1min, x1max, ... are coordinates
            x1min = zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100.
            x1max = zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100.
            x2min = xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
            x2max = xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
            # iloc1, iloc2, .. are grids
            jloc1 = int(dim_factor*len(xaxis)*xminloc/100.)
            jloc2 = int(dim_factor*len(xaxis)*xmaxloc/100.)
            iloc1 = int(dim_factor*len(zaxis)*zminloc/100.)
            iloc2 = int(dim_factor*len(zaxis)*zmaxloc/100.)

            kloc1 = 1
            kloc2 = 1
            
        else:   # 3D
            if self.main.sliceplane_panel[panelselect-1] == 'yx':
                xminloc = self.main.xminloc_panel[panelselect-1]
                xmaxloc = self.main.xmaxloc_panel[panelselect-1]
                yminloc = self.main.yminloc_panel[panelselect-1]
                ymaxloc = self.main.ymaxloc_panel[panelselect-1]
                x1min = xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                x1max = xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
                x2min = yaxis[0]+(yaxis[-1]-yaxis[0])*yminloc/100.
                x2max = yaxis[0]+(yaxis[-1]-yaxis[0])*ymaxloc/100.
                iloc1 = int(dim_factor*len(xaxis)*xminloc/100.)
                iloc2 = int(dim_factor*len(xaxis)*xmaxloc/100.)
                jloc1 = int(dim_factor*len(yaxis)*yminloc/100.)
                jloc2 = int(dim_factor*len(yaxis)*ymaxloc/100.)
                kloc1 = int(dim_factor*len(zaxis)*self.main.slicevalue_panel[panelselect-1]/50.)
                kloc2 = kloc1+1
                
            if self.main.sliceplane_panel[panelselect-1] == 'xz':
                xminloc = self.main.xminloc_panel[panelselect-1]
                xmaxloc = self.main.xmaxloc_panel[panelselect-1]
                zminloc = self.main.zminloc_panel[panelselect-1]
                zmaxloc = self.main.zmaxloc_panel[panelselect-1]
                x1min = zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100.
                x1max = zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100.
                x2min = xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                x2max = xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
                iloc1 = int(dim_factor*len(xaxis)*xminloc/100.)
                iloc2 = int(dim_factor*len(xaxis)*xmaxloc/100.)
                kloc1 = int(dim_factor*len(zaxis)*zminloc/100.)
                kloc2 = int(dim_factor*len(zaxis)*zmaxloc/100.)
                jloc1 = int(dim_factor*len(yaxis)*self.main.slicevalue_panel[panelselect-1]/50.)
                jloc2 = jloc1+1

            if self.main.sliceplane_panel[panelselect-1] == 'yz':
                yminloc = self.main.yminloc_panel[panelselect-1]
                ymaxloc = self.main.ymaxloc_panel[panelselect-1]
                zminloc = self.main.zminloc_panel[panelselect-1]
                zmaxloc = self.main.zmaxloc_panel[panelselect-1]
                x1min = zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100.
                x1max = zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100.
                x2min = yaxis[0]+(yaxis[-1]-yaxis[0])*yminloc/100.
                x2max = yaxis[0]+(yaxis[-1]-yaxis[0])*ymaxloc/100.
                jloc1 = int(dim_factor*len(yaxis)*yminloc/100.)
                jloc2 = int(dim_factor*len(yaxis)*ymaxloc/100.)
                kloc1 = int(dim_factor*len(zaxis)*zminloc/100.)
                kloc2 = int(dim_factor*len(zaxis)*zmaxloc/100.)
                iloc1 = int(dim_factor*len(xaxis)*self.main.slicevalue_panel[panelselect-1]/50)
                iloc2 = iloc1+1

        return x1min, x1max, x2min, x2max, iloc1, iloc2, jloc1, jloc2, kloc1, kloc2
