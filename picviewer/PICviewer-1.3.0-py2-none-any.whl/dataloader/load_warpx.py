import numpy as np

import yt
from yt.funcs import mylog
mylog.setLevel(0)

class LoadWarpx:

    def loadfield(self, 
                filepath,
                dim,
                dxfact,
                dyfact,
                dzfact,
                iteration, 
                field,
                amrlevel):

        fname =  filepath+'/plt'+str('%5.5d'%(iteration))
        ds = yt.load(fname)

        dim_factor = 2**amrlevel
        #print(amrlevel, dim_factor)

        #if dim == 3:
        #    nx, ny, nz = ds.domain_dimensions
        #else:
        #    nx, nz, ny = ds.domain_dimensions

        all_data_level = ds.covering_grid(level=amrlevel,
            left_edge=ds.domain_left_edge, dims=dim_factor*ds.domain_dimensions)
        if dim == 3:
            tempdata = all_data_level[field][::dxfact, ::dyfact, ::dzfact].d
        else:
            tempdata = all_data_level[field][::dxfact, ::dzfact, 0].d
            
            #tempdata = tempdata.T

        tempdata = np.float32(tempdata)

        return tempdata

    def loadparticle(self,
                filepath,
                dim,
                dpfact,
                iteration,
                species,
                variable):

        C = 2.99792458e8 # light speed

        fname =  filepath+'/plt'+str('%5.5d'%(iteration))
        ds = yt.load(fname)
        ad = ds.all_data()

        numpart = ds.particle_type_counts[species]
    
        if variable in ['x','y','z']:
            if dim == 2:
                if variable == 'z':
                    tempdata = ad[(species,'particle_position_y')][::dpfact[species]].d
                else:
                    tempdata = ad[(species,'particle_position_'+variable)][::dpfact[species]].d
            else:
                tempdata = ad[(species,'particle_position_'+variable)][::dpfact[species]].d
            
            tempdata = np.float32(tempdata)*1e6

        if variable in ['px','py','pz']:    
            tempdata = ad[(species,'particle_momentum_'+variable[1])][::dpfact[species]].d

            tempdata =np.float32(tempdata)/C

        if variable in ['w']:
            tempdata = ad[(species,'particle_weight')][::dpfact[species]].d

            tempdata =np.float32(tempdata)

        return tempdata

    def getAMRboundaries(self,
                filepath,
                dim,
                sliceplane,
                iteration,
                amrlevel):

        fname =  filepath+'/plt'+str('%5.5d'%(iteration))
        ds = yt.load(fname)

        xleftedge=[]
        xrightedge=[]
        zleftedge=[]
        zrightedge=[]

        
        if dim == 2:
            for grids in ds.index.grids:
                if grids.Level == amrlevel:
                    xleftedge.append(grids.LeftEdge[0].d*1.e6)
                    xrightedge.append(grids.RightEdge[0].d*1.e6)
                    zleftedge.append(grids.LeftEdge[1].d*1.e6)
                    zrightedge.append(grids.RightEdge[1].d*1.e6)

            x1leftedge = np.min(xleftedge)
            x1rightedge = np.max(xrightedge)
            x2leftedge = np.min(zleftedge)
            x2rightedge = np.max(zrightedge)
                
        else:

            yleftedge=[]
            yrightedge=[]
            for grids in ds.index.grids:
                if grids.Level == amrlevel:
                    xleftedge.append(grids.LeftEdge[0].d*1.e6)
                    xrightedge.append(grids.RightEdge[0].d*1.e6)
                    yleftedge.append(grids.LeftEdge[1].d*1.e6)
                    yrightedge.append(grids.RightEdge[1].d*1.e6)
                    zleftedge.append(grids.LeftEdge[2].d*1.e6)
                    zrightedge.append(grids.RightEdge[2].d*1.e6)
                        
            if sliceplane == 'yx':
                x1leftedge = np.min(xleftedge)
                x1rightedge = np.max(xrightedge)
                x2leftedge = np.min(yleftedge)
                x2rightedge = np.max(yrightedge)
            if sliceplane == 'xz':
                x1leftedge = np.min(zleftedge)
                x1rightedge = np.max(zrightedge)
                x2leftedge = np.min(xleftedge)
                x2rightedge = np.max(xrightedge)
            if sliceplane == 'yz':
                x1leftedge = np.min(zleftedge)
                x1rightedge = np.max(zrightedge)
                x2leftedge = np.min(yleftedge)
                x2rightedge = np.max(yrightedge)
                
            
        return x1leftedge, x1rightedge, x2leftedge, x2rightedge
