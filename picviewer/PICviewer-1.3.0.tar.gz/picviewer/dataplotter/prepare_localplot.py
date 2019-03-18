import numpy as np
from picviewer.dataplotter.makelocalplot import MakePlot

from picviewer.dataplotter.cic_histogram import particle_energy
from picviewer.dataloader.load_warpx import LoadWarpx
from picviewer.dataloader.load_openpmd import LoadOpenpmd


class PrepareLocalPlot():

    def __init__(self,Mainwindow):

        self.main = Mainwindow

        if self.main.dataformat == 'WarpX':
            self.loaddata = LoadWarpx()
        if self.main.dataformat == 'openPMD':
            self.loaddata = LoadOpenpmd()
        if self.main.dataformat == 'tristanMP':
            self.loaddata = LoadTristanmp()

        self.makeplot = MakePlot(self.main)


    def plotfield(self):

        panelselect = self.main.panelselect

        x1min, x1max, \
        x2min, x2max, \
        iloc1, iloc2, \
        jloc1, jloc2, \
        kloc1, kloc2 = self.getSpaceRanges(self.main.x1localmin,
                                            self.main.x1localmax,
                                            self.main.x2localmin,
                                            self.main.x2localmax)

        if self.main.dim == 2:

            self.makeplot.plotfield2D(
                            x1min,x1max,x2min,x2max,iloc1,iloc2,jloc1,jloc2)

        else:   # 3D
            self.makeplot.plotfield3D(
                            x1min,x1max,x2min,x2max,iloc1,iloc2,jloc1,jloc2,
                            kloc1,kloc2)

        
        self.main.subplot[panelselect-1].canvas.draw()


    def plotparticle(self):

        panelselect = self.main.panelselect

        x1min, x1max, \
        x2min, x2max, \
        dummy, dummy, \
        dummy, dummy, \
        dummy, dummy = self.getSpaceRanges(self.main.x1localmin,
                                            self.main.x1localmax,
                                            self.main.x2localmin,
                                            self.main.x2localmax)
        
        ####################################################################
        # We try to load particle data in case the local plot requries data that have not been loaded.
        # If the data have been read in memory, loading is skipped.
        species = self.main.species_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        
        for ind in range(2):
            variable = self.main.localphase_panel[self.main.panelselect-1][ind] 
            if variable in ['px','py','pz']:
                if (species,variable,tstep) in self.main.pdata_container.keys():
                    pass
                else:
                    self.main.pdata_container[(species,variable,tstep)] = \
                        self.loaddata.loadparticle(
                            self.main.filepath,
                            self.main.dim,
                            self.main.dpfact,
                            self.main.iterations[tstep-1], 
                            species,
                            variable)

        for ind in range(2):
            variable = self.main.localphase_panel[self.main.panelselect-1][ind] 
            if variable in ['ene']:
                if (species,variable,tstep) in self.main.pdata_container.keys():
                    pass
                else:
                    for var in ['px','py','pz']:
                        if (species,var,tstep) in self.main.pdata_container.keys():
                            pass
                        else:
                            self.main.pdata_container[(species,var,tstep)] = \
                            self.loaddata.loadparticle(
                                self.main.filepath,
                                self.main.dim,
                                self.main.dpfact,
                                self.main.iterations[tstep-1], 
                                species,
                                var)
                    self.main.pdata_container[(species,variable,tstep)] = \
                            particle_energy(
                                self.main.pdata_container[(species,'px',tstep)],
                                self.main.pdata_container[(species,'py',tstep)],
                                self.main.pdata_container[(species,'pz',tstep)])


        if self.main.localphase_panel[self.main.panelselect-1][0]  in ['fE']:
            variable ='ene'
            if (species,variable,tstep) in self.main.pdata_container.keys():
                pass
            else:
                for var in ['px','py','pz']:
                    if (species,var,tstep) in self.main.pdata_container.keys():
                        pass
                    else:
                        self.main.pdata_container[(species,var,tstep)] = \
                        self.loaddata.loadparticle(
                            self.main.filepath,
                            self.main.dim,
                            self.main.dpfact,
                            self.main.iterations[tstep-1], 
                            species,
                            var)
                self.main.pdata_container[(species,variable,tstep)] = \
                        particle_energy(
                            self.main.pdata_container[(species,'px',tstep)],
                            self.main.pdata_container[(species,'py',tstep)],
                            self.main.pdata_container[(species,'pz',tstep)])

        ### end loading data
        ####################################################################
        if self.main.dim == 2:

            local = np.where((self.main.pdata_container[(species,'z',tstep)] > x1min) & \
                                (self.main.pdata_container[(species,'z',tstep)] < x1max) & \
                                (self.main.pdata_container[(species,'x',tstep)] > x2min) & \
                                (self.main.pdata_container[(species,'x',tstep)] < x2max))

            self.makeplot.plotparticle(
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

                local2d = np.where((self.main.pdata_container[(species,'x',tstep)] > x1min) & \
                                (self.main.pdata_container[(species,'x',tstep)] < x1max) & \
                                (self.main.pdata_container[(species,'y',tstep)] > x2min) & \
                                (self.main.pdata_container[(species,'y',tstep)] < x2max))

                zvalue = zaxis[0]+(zaxis[-1]-zaxis[0])*(slicevalue/50.)
                width = (zaxis[-1]-zaxis[0])*(stride/50.)
                local1d = np.where((self.main.pdata_container[(species,'z',tstep)] > zvalue-.5*width) & \
                       (self.main.pdata_container[(species,'z',tstep)] < zvalue+.5*width))[0]

                local = np.intersect1d(local1d, local2d)
                
            if sliceplane == 'xz':

                local2d = np.where((self.main.pdata_container[(species,'z',tstep)] > x1min) & \
                                (self.main.pdata_container[(species,'z',tstep)] < x1max) & \
                                (self.main.pdata_container[(species,'x',tstep)] > x2min) & \
                                (self.main.pdata_container[(species,'x',tstep)] < x2max))

                yvalue = yaxis[0]+(yaxis[-1]-yaxis[0])*(slicevalue/50.)
                width = (yaxis[-1]-yaxis[0])*(stride/50.)
                local1d = np.where((self.main.pdata_container[(species,'y',tstep)] > yvalue-.5*width) & \
                       (self.main.pdata_container[(species,'y',tstep)] < yvalue+.5*width))[0]

                local = np.intersect1d(local1d, local2d)

            if sliceplane == 'yz':

                local2d = np.where((self.main.pdata_container[(species,'z',tstep)] > x1min) & \
                                (self.main.pdata_container[(species,'z',tstep)] < x1max) & \
                                (self.main.pdata_container[(species,'y',tstep)] > x2min) & \
                                (self.main.pdata_container[(species,'y',tstep)] < x2max))

                xvalue = xaxis[0]+(xaxis[-1]-xaxis[0])*(slicevalue/50.)
                width = (xaxis[-1]-xaxis[0])*(stride/50.)
                local1d = np.where((self.main.pdata_container[(species,'x',tstep)] > xvalue-.5*width) & \
                       (self.main.pdata_container[(species,'x',tstep)] < xvalue+.5*width))[0]

                local = np.intersect1d(local1d, local2d)

            self.makeplot.plotparticle(
                            x1min,x1max,
                            x2min,x2max,
                            local)

        self.main.subplot[panelselect-1].canvas.draw()

    
    def getSpaceRanges(self,
                    x1min,
                    x1max,
                    x2min,
                    x2max):
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

            if x2min < xaxis[0]:
                x2min = xaxis[1]
            if x2max > xaxis[-1]:
                x2max = xaxis[-2]

            if x1min < zaxis[0]:
                x1min = zaxis[1]
            if x1max > zaxis[-1]:
                x1max = zaxis[-2]

            if x2min > xaxis[-1]:
                x2min = xaxis[-3]
            if x2max < xaxis[0]:
                x2max = xaxis[2]
            
            if x1min > zaxis[-1]:
                x1min = zaxis[-3]
            if x1max < zaxis[0]:
                x1max = zaxis[2]

            # iloc1, iloc2, .. are grids
            jloc1 = dim_factor*np.where(xaxis >= x2min)[0][0]
            jloc2 = dim_factor*np.where(xaxis >= x2max)[0][0]
            iloc1 = dim_factor*np.where(zaxis >= x1min)[0][0]
            iloc2 = dim_factor*np.where(zaxis >= x1max)[0][0]


            kloc1 = 1
            kloc2 = 1
            
        else:   # 3D
            if self.main.sliceplane_panel[panelselect-1] == 'yx':

                if x2min < yaxis[0]:
                    x2min = yaxis[1]
                if x2max > yaxis[-1]:
                    x2max = yaxis[-2]

                if x1min < xaxis[0]:
                    x1min = xaxis[1]
                if x1max > xaxis[-1]:
                    x1max = xaxis[-2]

                if x2min > yaxis[-1]:
                    x2min = yaxis[-3]
                if x2max < yaxis[0]:
                    x2max = yaxis[2]
                
                if x1min > xaxis[-1]:
                    x1min = xaxis[-3]
                if x1max < xaxis[0]:
                    x1max = xaxis[2]
                
                iloc1 = dim_factor*np.where(xaxis >= x1min)[0][0]
                iloc2 = dim_factor*np.where(xaxis >= x1max)[0][0]
                jloc1 = dim_factor*np.where(yaxis >= x2min)[0][0]
                jloc2 = dim_factor*np.where(yaxis >= x2max)[0][0]
                kloc1 = int(dim_factor*len(zaxis)*self.main.slicevalue_panel[panelselect-1]/50.)
                kloc2 = kloc1+1

                
            if self.main.sliceplane_panel[panelselect-1] == 'xz':

                if x2min < xaxis[0]:
                    x2min = xaxis[1]
                if x2max > xaxis[-1]:
                    x2max = xaxis[-2]

                if x1min < zaxis[0]:
                    x1min = zaxis[1]
                if x1max > zaxis[-1]:
                    x1max = zaxis[-2]

                if x2min > xaxis[-1]:
                    x2min = xaxis[-3]
                if x2max < xaxis[0]:
                    x2max = xaxis[2]
                
                if x1min > zaxis[-1]:
                    x1min = zaxis[-3]
                if x1max < zaxis[0]:
                    x1max = zaxis[2]

                iloc1 = dim_factor*np.where(xaxis >= x2min)[0][0]
                iloc2 = dim_factor*np.where(xaxis >= x2max)[0][0]
                kloc1 = dim_factor*np.where(zaxis >= x1min)[0][0]
                kloc2 = dim_factor*np.where(zaxis >= x1max)[0][0]
                jloc1 = int(dim_factor*len(yaxis)*self.main.slicevalue_panel[panelselect-1]/50.)
                jloc2 = jloc1+1

                
            if self.main.sliceplane_panel[panelselect-1] == 'yz':

                if x2min < yaxis[0]:
                    x2min = yaxis[1]
                if x2max > yaxis[-1]:
                    x2max = yaxis[-2]

                if x1min < zaxis[0]:
                    x1min = zaxis[1]
                if x1max > zaxis[-1]:
                    x1max = zaxis[-2]

                if x2min > yaxis[-1]:
                    x2min = yaxis[-3]
                if x2max < yaxis[0]:
                    x2max = yaxis[2]
                
                if x1min > zaxis[-1]:
                    x1min = zaxis[-3]
                if x1max < zaxis[0]:
                    x1max = zaxis[2]

                jloc1 = dim_factor*np.where(yaxis >= x2min)[0][0]
                jloc2 = dim_factor*np.where(yaxis >= x2max)[0][0]
                kloc1 = dim_factor*np.where(zaxis >= x1min)[0][0]
                kloc2 = dim_factor*np.where(zaxis >= x1max)[0][0]
                iloc1 = int(dim_factor*len(xaxis)*self.main.slicevalue_panel[panelselect-1]/50)
                iloc2 = iloc1+1

        return x1min, x1max, x2min, x2max, iloc1, iloc2, jloc1, jloc2, kloc1, kloc2