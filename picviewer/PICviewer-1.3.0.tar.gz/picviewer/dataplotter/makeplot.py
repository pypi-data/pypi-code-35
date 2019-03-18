import matplotlib
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from .cic_histogram import histogram_cic_2d

import matplotlib.patches as patches

from picviewer.dataloader.load_warpx import LoadWarpx


class MakePlot():
    """
        Plot Data class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow

        #if self.main.dataformat == 'WarpX':
        #    from picviewer.dataloader.load_warpx import LoadWarpx

    def plotfield2D(self, 
                    x1min,
                    x1max,
                    x2min,
                    x2max,
                    iloc1, 
                    iloc2,
                    jloc1, 
                    jloc2):

        figure = self.main.figure
        nrow = self.main.nrow
        ncolumn = self.main.ncolumn
        panelselect = self.main.panelselect
        field = self.main.field_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        time = self.main.taxis[tstep-1]
        contrast = self.main.contrast_panel[panelselect-1]
        aspect = self.main.aspect_panel[panelselect-1]
        amrlevel = self.main.amrlevel_panel[self.main.panelselect-1]
        axis = self.main.axes[panelselect-1]
        cbar = self.main.cbars[panelselect-1]
                
        axis.remove()

        interpolation = 'nearest'
        
        fontmax = 10; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax

        xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'

        ax1 = figure.add_subplot(nrow,ncolumn,panelselect)

        if cbar:
            cbar.remove()

        fdata = self.main.fdata_container[(field,tstep,amrlevel)][jloc1:jloc2,iloc1:iloc2]

        vmin = fdata.min()*contrast/100.
        vmax = fdata.max()*contrast/100.

        im =  ax1.imshow(fdata, 
                interpolation=interpolation, cmap='jet',
                origin='lower', vmin = vmin, vmax = vmax, 
                extent=[x1min,x1max,x2min,x2max], 
                aspect=aspect)

        ax1.axes.set_xlim([x1min,x1max])
        ax1.axes.set_ylim([x2min,x2max])
        ax1.set_title(field+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
        ax1.set_xlabel(xtitle, fontsize=fontsize)
        ax1.set_ylabel(ytitle, fontsize=fontsize)

        ax = figure.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size=cbarwidth, pad=0.)
        cb = figure.colorbar(im, cax=cax)

        if amrlevel !=0:
            # loading AMR boundaries takes a time.. 
            # needs to be updated --> loading the boundaries at all time steps initially.
            x1leftedge, x1rightedge, x2leftedge, x2rightedge = \
                LoadWarpx().getAMRboundaries(
                                        self.main.filepath,
                                        self.main.dim,
                                        'dummy',
                                        self.main.iterations[tstep-1],
                                        amrlevel)

            ax1.plot([x1leftedge,x1leftedge],[x2leftedge,x2rightedge],':', linewidth=0.6, color='black')
            ax1.plot([x1leftedge,x1rightedge],[x2leftedge,x2leftedge],':', linewidth=0.6, color='black')
            ax1.plot([x1leftedge,x1rightedge],[x2rightedge,x2rightedge],':', linewidth=0.6, color='black')
            ax1.plot([x1rightedge,x1rightedge],[x2leftedge,x2rightedge],':', linewidth=0.6, color='black')



        if nrow < 4 and ncolumn < 4:
            ax1.axes.get_figure().tight_layout()

        return ax1, cb

    def plotfield3D(self, 
                    x1min,
                    x1max,
                    x2min,
                    x2max,
                    iloc1, 
                    iloc2,
                    jloc1, 
                    jloc2,
                    kloc1, 
                    kloc2):

        figure = self.main.figure
        nrow = self.main.nrow
        ncolumn = self.main.ncolumn
        panelselect = self.main.panelselect
        field = self.main.field_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        time = self.main.taxis[tstep-1]
        sliceplane = self.main.sliceplane_panel[panelselect-1]
        contrast = self.main.contrast_panel[panelselect-1]
        aspect = self.main.aspect_panel[panelselect-1]
        amrlevel = self.main.amrlevel_panel[self.main.panelselect-1]
        axis = self.main.axes[panelselect-1]
        cbar = self.main.cbars[panelselect-1]

        axis.remove()

        interpolation = 'nearest'
        
        fontmax = 11; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax


        fdata = self.main.fdata_container[(field,tstep,amrlevel)][iloc1:iloc2,jloc1:jloc2,kloc1:kloc2]

        if sliceplane == 'yx':
            xtitle = r'x ($\mu$m)'; ytitle = r'y ($\mu$m)'
            fdata = fdata[:,:,0].T
        if sliceplane == 'xz':
            xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'
            fdata = fdata[:,0,:]
        if sliceplane == 'yz':
            xtitle = r'z ($\mu$m)'; ytitle = r'y ($\mu$m)'
            fdata = fdata[0,:,:]

        ax1 = figure.add_subplot(nrow,ncolumn, panelselect)
    
        if cbar:
            cbar.remove()

        vmin = fdata.min()*contrast/100.
        vmax = fdata.max()*contrast/100.

        im =  ax1.imshow(fdata,
                    interpolation=interpolation, cmap='jet',
                    origin='lower', vmin = vmin, vmax = vmax, 
                    extent=[x1min,x1max,x2min,x2max], 
                    aspect=aspect)

        ax1.axes.set_xlim([x1min,x1max])
        ax1.axes.set_ylim([x2min,x2max])
        ax1.set_title(field+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
        ax1.set_xlabel(xtitle, fontsize=fontsize)
        ax1.set_ylabel(ytitle, fontsize=fontsize)

        ax = figure.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size=cbarwidth, pad=0.)
        cb = figure.colorbar(im, cax=cax)

        if amrlevel !=0:
            # loading AMR boundaries takes a time.. 
            # needs to be updated --> loading the boundaries at all time steps initially.
            x1leftedge, x1rightedge, x2leftedge, x2rightedge = \
                LoadWarpx().getAMRboundaries(
                                        self.main.filepath,
                                        self.main.dim,
                                        sliceplane,
                                        self.main.iterations[tstep-1],
                                        amrlevel)

            ax1.plot([x1leftedge,x1leftedge],[x2leftedge,x2rightedge],':', linewidth=0.6, color='black')
            ax1.plot([x1leftedge,x1rightedge],[x2leftedge,x2leftedge],':', linewidth=0.6, color='black')
            ax1.plot([x1leftedge,x1rightedge],[x2rightedge,x2rightedge],':', linewidth=0.6, color='black')
            ax1.plot([x1rightedge,x1rightedge],[x2leftedge,x2rightedge],':', linewidth=0.6, color='black')

            #rect = patches.Rectangle((x1leftedge, x2leftedge),
            #                x1rightedge-x1leftedge, x2rightedge-x2leftedge,
            #                linestyle=':', linewidth=0.6,edgecolor='black',facecolor='none')

            #ax1.add_patch(rect)

        if nrow < 4 and ncolumn < 4:
            ax1.axes.get_figure().tight_layout()

        return ax1, cb

    def plotparticle(self,
                    x1min,
                    x1max,
                    x2min,
                    x2max,
                    local):

        figure = self.main.figure
        nrow = self.main.nrow
        ncolumn = self.main.ncolumn
        panelselect = self.main.panelselect
        species = self.main.species_panel[panelselect-1]
        phase = self.main.phase_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        time = self.main.taxis[tstep-1]
        #contrast = self.main.contrast_panel[panelselect-1]
        aspect = self.main.aspect_panel[panelselect-1]
        cbar = self.main.cbars[(panelselect-1)]
        axis = self.main.axes[panelselect-1]

        dim = self.main.dim

        axis.remove()

        interpolation = 'nearest'

        fontmax = 10; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax

        title = species+' '+phase[0]+'-'+phase[1]

        xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'
        nbin = 300

        ax1 = figure.add_subplot(nrow,ncolumn,panelselect)
        #self.plot.cla()

        if cbar:
                cbar.remove()

        if len(self.main.pdata_container[(species,'w',tstep)]) > 0 :
        
            ###################
            # x-axis
            ###################
            if phase[1] in ['px','py','pz']:
                if dim == 2:
                    p1min = np.min(self.main.pdata_container[(species,phase[1],tstep)])
                    p1max = np.max(self.main.pdata_container[(species,phase[1],tstep)])
                else:
                    p1min = np.min(self.main.pdata_container[(species,phase[1],tstep)][local])
                    p1max = np.max(self.main.pdata_container[(species,phase[1],tstep)][local])
                xtitle = r'%s ($c$)'%(phase[1])
                # if the minimunm and maximum values are the same, 
                #   an error occurs in the histogram.
            elif phase[1] in ['ene']:
                if dim == 2:
                    p1min = np.min(self.main.pdata_container[(species,phase[1],tstep)])
                    p1max = np.max(self.main.pdata_container[(species,phase[1],tstep)])
                else:
                    p1min = np.min(self.main.pdata_container[(species,phase[1],tstep)][local])
                    p1max = np.max(self.main.pdata_container[(species,phase[1],tstep)][local])
                xtitle = r'%s ($\gamma$-1)'%(phase[1])
            elif phase[1] in ['x','y','z']:
                p1min = x1min
                p1max = x1max
                xtitle = r'%s ($\mu$m)'%(phase[1])
       
            ###################
            # y-axis
            ###################
            if phase[0] in ['px','py','pz']:
                if dim == 2:
                    p2min = np.min(self.main.pdata_container[(species,phase[0],tstep)])
                    p2max = np.max(self.main.pdata_container[(species,phase[0],tstep)])
                else:
                    p2min = np.min(self.main.pdata_container[(species,phase[0],tstep)][local])
                    p2max = np.max(self.main.pdata_container[(species,phase[0],tstep)][local])
                ytitle = r'%s ($c$)'%(phase[0])
            elif phase[0] in ['ene']:
                if dim == 2:
                    p2min = np.min(self.main.pdata_container[(species,phase[0],tstep)])
                    p2max = np.max(self.main.pdata_container[(species,phase[0],tstep)])
                else:
                    p2min = np.min(self.main.pdata_container[(species,phase[0],tstep)][local])
                    p2max = np.max(self.main.pdata_container[(species,phase[0],tstep)][local])
                ytitle = r'%s ($\gamma$-1)'%(phase[0])
            elif phase[0] in ['x','y','z']:
                p2min = x2min
                p2max = x2max
                ytitle = r'%s ($\mu$m)'%(phase[0])

            if p1min == p1max:
                if p1min != 0:
                    p1min = p1min*.5
                    p1max = p1min*3.
                else:
                    p1max = 1.0
            if p2min == p2max:
                if p2min != 0:
                    p2min = p2min*.5
                    p2max = p2min*3.
                else:
                    p2max = 1.0

            if dim == 2:
                histogram = histogram_cic_2d( self.main.pdata_container[(species,phase[1],tstep)], 
                            self.main.pdata_container[(species,phase[0],tstep)], 
                            self.main.pdata_container[(species,'w',tstep)], 
                            nbin, p1min, p1max, nbin, p2min, p2max)   
            else:
                histogram = histogram_cic_2d( self.main.pdata_container[(species,phase[1],tstep)][local], 
                            self.main.pdata_container[(species,phase[0],tstep)][local], 
                            self.main.pdata_container[(species,'w',tstep)][local], 
                            nbin, p1min, p1max, nbin, p2min, p2max)   

            vmax=np.max(histogram)
            vmin = vmax*1.e-4
            #vmax *= contrast/100.
            #vmin *= 100./contrast
            logthresh=-np.log10(vmin)
            
            im = ax1.imshow( histogram.T, 
                        origin='lower', extent=[ p1min,p1max,p2min,p2max], 
                        aspect=aspect, interpolation=interpolation, cmap='jet',
                        vmin=vmin, vmax=vmax, 
                        norm=matplotlib.colors.LogNorm(10**-logthresh))

            ax1.axes.set_xlim([p1min,p1max])
            ax1.axes.set_ylim([p2min,p2max])
            ax1.set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
            ax1.set_xlabel(xtitle, fontsize=fontsize)
            ax1.set_ylabel(ytitle, fontsize=fontsize)
            ax = figure.gca()
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size=cbarwidth, pad=0.)
            cb = figure.colorbar(im, cax=cax)

        else:

            if phase[1] in ['px','py','pz']:
                xtitle = r'%s ($c$)'%(phase[1])
            elif phase[1] in ['ene']:
                xtitle = r'%s ($\gamma$-1)'%(phase[1])
            elif phase[1] in ['x','y','z']:
                xtitle = r'%s ($\mu$m)'%(phase[1])
            if phase[0] in ['px','py','pz']:
                ytitle = r'%s ($c$)'%(phase[0])
            elif phase[0] in ['ene']:
                ytitle = r'%s ($\gamma$-1)'%(phase[0])
            elif phase[0] in ['x','y','z']:
                ytitle = r'%s ($\mu$m)'%(phase[0])

            #self.plot.axes.set_xlim([x1min,x1max])
            #self.plot.axes.set_ylim([x2min,x2max])
            ax1.set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
            ax1.set_xlabel(xtitle, fontsize=fontsize)
            ax1.set_ylabel(ytitle, fontsize=fontsize)

            cb = []
    
        #if nrow < 4 or ncolumn < 4:
        ax1.axes.get_figure().tight_layout()

        return ax1, cb

    def makeplotsync2D(self):

        figure = self.main.figure
        nrow = self.main.nrow 
        ncolumn = self.main.ncolumn
        field_select_panel = self.main.field_select_panel
        field_panel = self.main.field_panel
        species_panel = self.main.species_panel
        phase_panel = self.main.phase_panel
        tstep_panel = self.main.tstep_panel
        taxis = self.main.taxis
        xaxis_dic = self.main.xaxis_dic
        zaxis_dic = self.main.zaxis_dic
        xminloc_panel = self.main.xminloc_panel
        xmaxloc_panel = self.main.xmaxloc_panel
        zminloc_panel = self.main.zminloc_panel
        zmaxloc_panel = self.main.zmaxloc_panel
        contrast_panel = self.main.contrast_panel
        aspect_panel = self.main.aspect_panel
        amrlevel_panel = self.main.amrlevel_panel

        figure.clear()

        interpolation = 'nearest'
        
        fontmax = 10; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax
        axes={}
        cbars={}

        for l in np.arange(nrow*ncolumn):

            tstep = tstep_panel[l]
            time = taxis[tstep-1]
            xaxis = xaxis_dic[tstep-1]
            zaxis = zaxis_dic[tstep-1]
            
            amrlevel = amrlevel_panel[l]
            dim_factor = 2**amrlevel

            contrast = contrast_panel[l]
            aspect = aspect_panel[l]

            axes[l] = figure.add_subplot(nrow,ncolumn,l+1)

            x1min = zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc_panel[l]/100.
            x1max = zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc_panel[l]/100.
            x2min = xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc_panel[l]/100.
            x2max = xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc_panel[l]/100.

            if field_select_panel[l]:
                # field plot
                field=field_panel[l]
            
                xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'
                iloc1 = dim_factor*int(len(zaxis)*zminloc_panel[l]/100.)
                iloc2 = dim_factor*int(len(zaxis)*zmaxloc_panel[l]/100.)
                jloc1 = dim_factor*int(len(xaxis)*xminloc_panel[l]/100.)
                jloc2 = dim_factor*int(len(xaxis)*xmaxloc_panel[l]/100.)

                vmin = self.main.fdata_container[(field, tstep, amrlevel)][jloc1:jloc2,iloc1:iloc2].min()
                vmax = self.main.fdata_container[(field, tstep, amrlevel)][jloc1:jloc2,iloc1:iloc2].max()
                vmin = vmin*contrast/100.
                vmax = vmax*contrast/100.

                im =  axes[l].imshow(self.main.fdata_container[(field, tstep, amrlevel)][jloc1:jloc2,iloc1:iloc2], 
                    interpolation=interpolation, cmap='jet',
                    origin='lower', vmin = vmin, vmax = vmax, extent=[x1min,x1max,x2min,x2max], aspect=aspect)

                axes[l].axes.set_xlim([x1min,x1max])
                axes[l].axes.set_ylim([x2min,x2max])
                axes[l].set_title(field+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                axes[l].set_xlabel(xtitle, fontsize=fontsize)
                axes[l].set_ylabel(ytitle, fontsize=fontsize)

                ax = figure.gca()
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size=cbarwidth, pad=0.)
                cb = figure.colorbar(im, cax=cax)

            else:   # particle plot
                species = species_panel[l]
            
                # pahse is a tuple, i.e., (px,x) --> px is the x2 axis (y-axis), x is the x1 axis (x-axis)
                phase = phase_panel[l]

                title = species+' '+phase[0]+'-'+phase[1]
                nbin = 300

                if len(self.main.pdata_container[(species, 'w', tstep)])  > 0:
                
                    # x1-axis (or x-axis) variables
                    if phase[1] in ['px','py','pz']:
                        p1min = np.min(self.main.pdata_container[(species, phase[1], tstep)])
                        p1max = np.max(self.main.pdata_container[(species, phase[1], tstep)])
                        xtitle = r'%s ($c$)'%(phase[1])
                    elif phase[1] in ['ene']:
                        p1min = np.min(self.main.pdata_container[(species, phase[1], tstep)])
                        p1max = np.max(self.main.pdata_container[(species, phase[1], tstep)])
                        xtitle = r'%s ($\gamma$-1)'%(phase[1])
                    elif phase[1] in ['x','y','z']:
                        p1min = x1min
                        p1max = x1max
                        xtitle = r'%s ($\mu$m)'%(phase[1])

                    # x2-axis (y-axis) variables
                    if phase[0] in ['px','py','pz']:
                        p2min = np.min(self.main.pdata_container[(species, phase[0], tstep)])
                        p2max = np.max(self.main.pdata_container[(species, phase[0], tstep)])
                        ytitle = r'%s ($c$)'%(phase[0])
                    elif phase[0] in ['ene']:
                        p2min = np.min(self.main.pdata_container[(species, phase[0], tstep)])
                        p2max = np.max(self.main.pdata_container[(species, phase[0], tstep)])
                        ytitle = r'%s ($\gamma$-1)'%(phase[0])
                    elif phase[0] in ['x','y','z']:
                        p2min = x2min
                        p2max = x2max
                        ytitle = r'%s ($\mu$m)'%(phase[0])

                    if p1min == p1max:
                        if p1min != 0:
                            p1min = p1min*.5
                            p1max = p1min*3.
                        else:
                            p1max = 1.0
                    if p2min == p2max:
                        if p2min != 0:
                            p2min = p2min*.5
                            p2max = p2min*3.
                        else:
                            p2max = 1.0

                    histogram = histogram_cic_2d( 
                            self.main.pdata_container[(species, phase[1], tstep)],
                            self.main.pdata_container[(species, phase[0], tstep)],    
                            self.main.pdata_container[(species, 'w', tstep)], 
                            nbin, p1min, p1max, nbin, p2min, p2max)   

                    vmax=np.max(histogram)
                    vmin = vmax*1.e-4
                    #vmax *= contrast/100.
                    #vmin *= 100./contrast
                    logthresh=-np.log10(vmin)
                    
                    im = axes[l].imshow( histogram.T, 
                                    origin='lower', extent=[ p1min,p1max,p2min,p2max ], 
                                    aspect=aspect, interpolation=interpolation, cmap='jet',
                                    vmin=vmin, vmax=vmax,
                                    norm=matplotlib.colors.LogNorm(10**-logthresh))

                    axes[l].axes.set_xlim([p1min,p1max])
                    axes[l].axes.set_ylim([p2min,p2max])
                    axes[l].set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                    axes[l].set_xlabel(xtitle, fontsize=fontsize)
                    axes[l].set_ylabel(ytitle, fontsize=fontsize)
                    ax = figure.gca()
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size=cbarwidth, pad=0.)
                    cb = figure.colorbar(im, cax=cax)

                else: 

                    # x1-axis (or x-axis) variables
                    if phase[1] in ['px','py','pz']:
                        xtitle = r'%s ($c$)'%(phase[1])
                    elif phase[1] in ['ene']:
                        xtitle = r'%s ($\gamma$-1)'%(phase[1])
                    elif phase[1] in ['x','y','z']:
                        xtitle = r'%s ($\mu$m)'%(phase[1])
                    # x2-axis (y-axis) variables
                    if phase[0] in ['px','py','pz']:
                        ytitle = r'%s ($c$)'%(phase[0])
                    elif phase[0] in ['ene']:
                        ytitle = r'%s ($\gamma$-1)'%(phase[0])
                    elif phase[0] in ['x','y','z']:
                        ytitle = r'%s ($\mu$m)'%(phase[0])

                    #self.plot.axes.set_xlim([p1min,p1max])
                    #self.plot.axes.set_ylim([p2min,p2max])
                    axes[l].set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                    axes[l].set_xlabel(xtitle, fontsize=fontsize)
                    axes[l].set_ylabel(ytitle, fontsize=fontsize)

                    cb=[]
                
            cbars[l]= cb

            if nrow < 4 and ncolumn < 4:
                axes[l].axes.get_figure().tight_layout()

        return axes, cbars
        

    def makeplotsync3D(self, loc_container):


        figure = self.main.figure
        nrow = self.main.nrow 
        ncolumn = self.main.ncolumn
        field_select_panel = self.main.field_select_panel
        field_panel = self.main.field_panel
        species_panel = self.main.species_panel
        phase_panel = self.main.phase_panel
        tstep_panel = self.main.tstep_panel
        taxis = self.main.taxis
        sliceplane_panel = self.main.sliceplane_panel
        slicevalue_panel = self.main.slicevalue_panel
        xaxis_dic = self.main.xaxis_dic
        yaxis_dic = self.main.yaxis_dic
        zaxis_dic = self.main.zaxis_dic
        xminloc_panel = self.main.xminloc_panel
        xmaxloc_panel = self.main.xmaxloc_panel
        yminloc_panel = self.main.yminloc_panel
        ymaxloc_panel = self.main.ymaxloc_panel
        zminloc_panel = self.main.zminloc_panel
        zmaxloc_panel = self.main.zmaxloc_panel
        amrlevel_panel = self.main.amrlevel_panel
        contrast_panel = self.main.contrast_panel
        aspect_panel = self.main.aspect_panel

        figure.clear()

        interpolation = 'nearest'
        
        fontmax = 10; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax

        axes={}
        cbars={}

        for l in np.arange(nrow*ncolumn):
            
            axes[l] = figure.add_subplot(nrow,ncolumn,l+1)

            amrlevel = amrlevel_panel[l]
            dim_factor = 2**amrlevel

            contrast = contrast_panel[l]
            aspect = aspect_panel[l]

            tstep = tstep_panel[l]
            time = taxis[tstep-1]
            xaxis = xaxis_dic[tstep-1]
            yaxis = yaxis_dic[tstep-1]
            zaxis = zaxis_dic[tstep-1]

            sliceplane = sliceplane_panel[l]
            slicevalue = slicevalue_panel[l]
            xminloc = xminloc_panel[l]
            xmaxloc = xmaxloc_panel[l]
            yminloc = yminloc_panel[l]
            ymaxloc = ymaxloc_panel[l]
            zminloc = zminloc_panel[l]
            zmaxloc = zmaxloc_panel[l]

            if sliceplane == 'yx':
                x1min = xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                x1max = xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.
                x2min = yaxis[0]+(yaxis[-1]-yaxis[0])*yminloc/100.
                x2max = yaxis[0]+(yaxis[-1]-yaxis[0])*ymaxloc/100.

            if sliceplane == 'xz':
                    xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'
                    x1min = zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100.
                    x1max = zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100.
                    x2min = xaxis[0]+(xaxis[-1]-xaxis[0])*xminloc/100.
                    x2max = xaxis[0]+(xaxis[-1]-xaxis[0])*xmaxloc/100.

            if sliceplane == 'yz':
                    xtitle = r'z ($\mu$m)'; ytitle = r'y ($\mu$m)'
                    x1min = zaxis[0]+(zaxis[-1]-zaxis[0])*zminloc/100.
                    x1max = zaxis[0]+(zaxis[-1]-zaxis[0])*zmaxloc/100.
                    x2min = yaxis[0]+(yaxis[-1]-yaxis[0])*yminloc/100.
                    x2max = yaxis[0]+(yaxis[-1]-yaxis[0])*ymaxloc/100.

            if field_select_panel[l]:
                # field plot
                field=field_panel[l]

                if sliceplane == 'yx':
                    xtitle = r'x ($\mu$m)'; ytitle = r'y ($\mu$m)'
                    iloc1 = dim_factor*int(len(xaxis)*xminloc/100.)
                    iloc2 = dim_factor*int(len(xaxis)*xmaxloc/100.)
                    jloc1 = dim_factor*int(len(yaxis)*yminloc/100.)
                    jloc2 = dim_factor*int(len(yaxis)*ymaxloc/100.)
                    kloc = int(dim_factor*len(zaxis)*slicevalue/50.)

                    vmin = self.main.fdata_container[(field, tstep, amrlevel)][iloc1:iloc2,jloc1:jloc2,kloc].min()
                    vmax = self.main.fdata_container[(field, tstep, amrlevel)][iloc1:iloc2,jloc1:jloc2,kloc].max()
                    vmin = vmin*contrast/100.
                    vmax = vmax*contrast/100.

                    im =  axes[l].imshow(self.main.fdata_container[(field, tstep, amrlevel)][iloc1:iloc2,jloc1:jloc2,kloc].T, 
                    interpolation=interpolation, cmap='jet',
                    origin='lower', vmin=vmin, vmax=vmax, extent=[x1min,x1max,x2min,x2max], aspect=aspect)

                if sliceplane == 'xz':
                    xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'
                    iloc1 = int(dim_factor*len(zaxis)*zminloc/100.)
                    iloc2 = int(dim_factor*len(zaxis)*zmaxloc/100.)
                    jloc1 = int(dim_factor*len(xaxis)*xminloc/100.)
                    jloc2 = int(dim_factor*len(xaxis)*xmaxloc/100.)
                    kloc = int(dim_factor*len(yaxis)*slicevalue/50)

                    im =  axes[l].imshow(self.main.fdata_container[(field, tstep, amrlevel)][jloc1:jloc2,kloc,iloc1:iloc2], 
                    interpolation=interpolation, cmap='jet',
                    origin='lower', extent=[x1min,x1max,x2min,x2max], aspect=aspect)

                if sliceplane == 'yz':
                    xtitle = r'z ($\mu$m)'; ytitle = r'y ($\mu$m)'
                    iloc1 = int(dim_factor*len(zaxis)*zminloc/100.)
                    iloc2 = int(dim_factor*len(zaxis)*zmaxloc/100.)
                    jloc1 = int(dim_factor*len(yaxis)*yminloc/100.)
                    jloc2 = int(dim_factor*len(yaxis)*ymaxloc/100.)
                    kloc = int(dim_factor*len(xaxis)*slicevalue/50)
                    
                    im =  axes[l].imshow(self.main.fdata_container[(field, tstep, amrlevel)][kloc,jloc1:jloc2,iloc1:iloc2],
                    interpolation=interpolation, cmap='jet',
                    origin='lower', extent=[x1min,x1max,x2min,x2max], aspect=aspect)

                axes[l].axes.set_xlim([x1min,x1max])
                axes[l].axes.set_ylim([x2min,x2max])
                axes[l].set_title(field+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                axes[l].set_xlabel(xtitle, fontsize=fontsize)
                axes[l].set_ylabel(ytitle, fontsize=fontsize)

                ax = figure.gca()
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size=cbarwidth, pad=0.)
                cb = figure.colorbar(im, cax=cax)

            else:   # particle plot
                species = species_panel[l]
                phase = phase_panel[l]

                title = species+' '+phase[0]+'-'+phase[1]
                nbin = 300

                loc = loc_container[l]

                # there must be at least one particle for histogram
                if len(loc)  > 0:
               
                    if phase[1] in ['px','py','pz']:
                        p1min = np.min(self.main.pdata_container[(species, phase[1], tstep)][loc])
                        p1max = np.max(self.main.pdata_container[(species, phase[1], tstep)][loc])
                        xtitle = r'%s ($c$)'%(phase[1])
                    elif phase[1] in ['ene']:
                        p1min = np.min(self.main.pdata_container[(species, phase[1], tstep)][loc])
                        p1max = np.max(self.main.pdata_container[(species, phase[1], tstep)][loc])
                        xtitle = r'%s ($\gamma$-1)'%(phase[1])
                    elif phase[1] in ['x','y','z']:
                        p1min = x1min
                        p1max = x1max
                        xtitle = r'%s ($\mu$m)'%(phase[1])
                    if phase[0] in ['px','py','pz']:
                        p2min = np.min(self.main.pdata_container[(species, phase[0], tstep)][loc])
                        p2max = np.max(self.main.pdata_container[(species, phase[0], tstep)][loc])
                        ytitle = r'%s ($c$)'%(phase[0])
                    elif phase[0] in ['ene']:
                        p2min = np.min(self.main.pdata_container[(species, phase[0], tstep)][loc])
                        p2max = np.max(self.main.pdata_container[(species, phase[0], tstep)][loc])
                        ytitle = r'%s ($\gamma$-1)'%(phase[0])
                    elif phase[0] in ['x','y','z']:
                        p2min = x2min
                        p2max = x2max
                        ytitle = r'%s ($\mu$m)'%(phase[0])

                    if p1min == p1max:
                        if p1min != 0:
                            p1min = p1min*.5
                            p1max = p1min*3.
                        else:
                            p1max = 1.0
                    if p2min == p2max:
                        if p2min != 0:
                            p2min = p2min*.5
                            p2max = p2min*3.
                        else:
                            p2max = 1.0

                    histogram = histogram_cic_2d( 
                            self.main.pdata_container[(species, phase[1], tstep)][loc],
                            self.main.pdata_container[(species, phase[0], tstep)][loc],    
                            self.main.pdata_container[(species, 'w', tstep)][loc], nbin, p1min, p1max, nbin, p2min, p2max)   

                    vmax=np.max(histogram)
                    vmin = vmax*1.e-4
                    #vmax *= contrast/100.
                    #vmin *= 100./contrast
                    logthresh=-np.log10(vmin)
                    
                    im = axes[l].imshow( histogram.T, 
                                    origin='lower', extent=[ p1min,p1max,p2min,p2max ], 
                                    aspect=aspect, interpolation=interpolation, cmap='jet',
                                    vmin=vmin, vmax=vmax,
                                    norm=matplotlib.colors.LogNorm(10**-logthresh))

                    axes[l].axes.set_xlim([p1min,p1max])
                    axes[l].axes.set_ylim([p2min,p2max])
                    axes[l].set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                    axes[l].set_xlabel(xtitle, fontsize=fontsize)
                    axes[l].set_ylabel(ytitle, fontsize=fontsize)
                    ax = figure.gca()
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size=cbarwidth, pad=0.)
                    cb = figure.colorbar(im, cax=cax)

                else: 

                    if phase[1] in ['px','py','pz']:
                        xtitle = r'%s ($c$)'%(phase[1])
                    elif phase[1] in ['ene']:
                        xtitle = r'%s ($\gamma$-1)'%(phase[1])
                    elif phase[1] in ['x','y','z']:
                        xtitle = r'%s ($\mu$m)'%(phase[1])

                    if phase[0] in ['px','py','pz']:
                        ytitle = r'%s ($c$)'%(phase[0])
                    elif phase[0] in ['ene']:
                        ytitle = r'%s ($\gamma$-1)'%(phase[0])
                    elif phase[0] in ['x','y','z']:
                        ytitle = r'%s ($\mu$m)'%(phase[0])

                    #self.plot.axes.set_xlim([p1min,p1max])
                    #self.plot.axes.set_ylim([p2min,p2max])
                    axes[l].set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                    axes[l].set_xlabel(xtitle, fontsize=fontsize)
                    axes[l].set_ylabel(ytitle, fontsize=fontsize)

                    cb=[]
                    

            cbars[l]= cb

            if nrow < 4 and ncolumn < 4:
                axes[l].axes.get_figure().tight_layout()

        return axes, cbars



    def locallineplot2D(self, 
                figure, 
                nrow, 
                ncolumn, 
                field,
                panel_select,
                time,
                laxis, 
                ldata):
                
        interpolation = 'spline16'
        
        fontmax = 10; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax

        xtitle = r'l ($\mu$m)'; ytitle = field
        
        self.plot = figure.add_subplot(nrow,ncolumn,panel_select)
        self.plot.cla()

        self.plot.plot(laxis, ldata)

        self.plot.set_title(field+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
        self.plot.set_xlabel(xtitle, fontsize=fontsize)
        self.plot.set_ylabel(ytitle, fontsize=fontsize)

        #if nrow < 4 or ncolumn < 4:
        #        self.plot.axes.get_figure().tight_layout()


    def localcontourplot2D(self, 
                figure, 
                fdata, 
                nrow, 
                ncolumn, 
                field,
                panel_select,
                time,
                x1min,
                x1max,
                x2min,
                x2max,
                aspect):

        interpolation = 'nearest'
        
        fontmax = 11; fontmin = 5.
        barmax = 0.12; barmin = 0.05
        matplotlib.rc('xtick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        matplotlib.rc('ytick', labelsize=int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax))
        fontsize = int((fontmin-fontmax)/(30-1)*(nrow*ncolumn-1)+fontmax)
        cbarwidth = (barmin-barmax)/(30-1)*(nrow*ncolumn-1)+barmax

        xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'

        self.plot = figure.add_subplot(nrow,ncolumn,panel_select)
        self.plot.cla()

        im =  self.plot.imshow(fdata, interpolation=interpolation, cmap='jet',
            origin='lower', extent=[x1min,x1max,x2min,x2max], aspect=aspect)

        self.plot.axes.set_xlim([x1min,x1max])
        self.plot.axes.set_ylim([x2min,x2max])
        self.plot.set_title(field+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
        self.plot.set_xlabel(xtitle, fontsize=fontsize)
        self.plot.set_ylabel(ytitle, fontsize=fontsize)

        ax = figure.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size=cbarwidth, pad=0.)
        cb = figure.colorbar(im, cax=cax)

        #if nrow < 4 or ncolumn < 4:
        #        self.plot.axes.get_figure().tight_layout()
