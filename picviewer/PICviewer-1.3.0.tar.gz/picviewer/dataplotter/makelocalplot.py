import matplotlib
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from .cic_histogram import histogram_cic_2d, histogram_cic_1d

#from matplotlib.figure import Figure

class MakePlot():
    """
        Plot Data class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow
        

    def plotfield2D(self,
                    x1min,
                    x1max,
                    x2min,
                    x2max,
                    iloc1, 
                    iloc2,
                    jloc1, 
                    jloc2):

        panelselect = self.main.panelselect
        figure = self.main.subplot[panelselect-1].figure
        field = self.main.field_panel[panelselect-1]
        phase = self.main.localfield_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        time = self.main.taxis[tstep-1]
        #contrast = self.main.contrast_panel[panelselect-1]
        aspect = self.main.aspect_panel[panelselect-1]
        #axis = self.main.subaxes[panelselect-1]
        #cbar = self.main.subcbars[panelselect-1]
        amrlevel = self.main.amrlevel_panel[self.main.panelselect-1]
                

        figure.clear()

        interpolation = 'nearest'
        
        fontmax = 10
        barmax = 0.12
        matplotlib.rc('xtick', labelsize=fontmax)
        matplotlib.rc('ytick', labelsize=fontmax)
        fontsize = fontmax
        cbarwidth = barmax

        xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'

        ax1 = figure.add_subplot(111)

        fdata = self.main.fdata_container[(field,tstep,amrlevel)][jloc1:jloc2,iloc1:iloc2]

        vmin = fdata.min()#*contrast/100.
        vmax = fdata.max()#*contrast/100.

        if phase == 'field':

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
            figure.colorbar(im, cax=cax)

        if phase == 'FFT':

            fft2d = np.fft.fft2(fdata)
            fft2d = np.fft.fftshift(fft2d)
            fft2d = np.abs(fft2d)

            kxmin = np.pi/(x1min-(x1min+x1max)*.5)
            kxmax = np.pi/(x1max-(x1min+x1max)*.5)
            kymin = np.pi/(x2min-(x2min+x2max)*.5)
            kymax = np.pi/(x2max-(x2min+x2max)*.5)

            ax1.imshow(fft2d, interpolation=interpolation, cmap='jet',
                origin='lower', extent=[ kxmin,kxmax,kymin,kymax ], aspect=aspect)

            ax1.axes.set_xlim([kxmin,kxmax])
            ax1.axes.set_ylim([kymin,kymax])
            ax1.set_title(field+'FFT  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
            ax1.set_xlabel(r'$k_x$ (1/$\mu$m)', fontsize=fontsize)
            ax1.set_ylabel(r'$k_y$ (1/$\mu$m)', fontsize=fontsize)

        ax1.axes.get_figure().tight_layout()


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

        panelselect = self.main.panelselect
        figure = self.main.subplot[panelselect-1].figure
        field = self.main.field_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        time = self.main.taxis[tstep-1]
        sliceplane = self.main.sliceplane_panel[panelselect-1]
        #contrast = self.main.contrast_panel[panelselect-1]
        aspect = self.main.aspect_panel[panelselect-1]
        #axis = self.main.subaxes[panelselect-1]
        #cbar = self.main.subcbars[panelselect-1]
        phase = self.main.localfield_panel[panelselect-1]
        amrlevel = self.main.amrlevel_panel[self.main.panelselect-1]

        figure.clear()
        
        interpolation = 'nearest'
        
        fontmax = 10
        barmax = 0.12
        matplotlib.rc('xtick', labelsize=fontmax)
        matplotlib.rc('ytick', labelsize=fontmax)
        fontsize = fontmax
        cbarwidth = barmax

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

        ax1 = figure.add_subplot(111)
    
        vmin = fdata.min()#*contrast/100.
        vmax = fdata.max()#*contrast/100.

        if phase == 'field':

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
            figure.colorbar(im, cax=cax)


        if phase == 'FFT':

            fft2d = np.fft.fft2(fdata)
            fft2d = np.fft.fftshift(fft2d)
            fft2d = np.abs(fft2d)

            kxmin = np.pi/(x1min-(x1min+x1max)*.5)
            kxmax = np.pi/(x1max-(x1min+x1max)*.5)
            kymin = np.pi/(x2min-(x2min+x2max)*.5)
            kymax = np.pi/(x2max-(x2min+x2max)*.5)

            #zoom = 0.
            #kxmin = (kxmax-kxmin)*zoom/100.+kxmin
            #kxmax = (kxmax-kxmin)*zoom/100.+kxmin
            #kymin = (kymax-kymin)*zoom/100.+kymin
            #kymax = (kymax-kymin)*zoom/100.+kymin

            ax1.imshow(fft2d, interpolation=interpolation, cmap='jet',
                origin='lower', extent=[ kxmin,kxmax,kymin,kymax ], aspect=aspect)

            ax1.axes.set_xlim([kxmin,kxmax])
            ax1.axes.set_ylim([kymin,kymax])
            ax1.set_title(field+'FFT  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
            ax1.set_xlabel(r'$k_x$ (1/$\mu$m)', fontsize=fontsize)
            ax1.set_ylabel(r'$k_y$ (1/$\mu$m)', fontsize=fontsize)

        ax1.axes.get_figure().tight_layout()


    def plotparticle(self,
                    x1min,
                    x1max,
                    x2min,
                    x2max,
                    local):

        panelselect = self.main.panelselect
        figure = self.main.subplot[panelselect-1].figure
        species = self.main.species_panel[panelselect-1]
        phase = self.main.localphase_panel[panelselect-1]
        tstep = self.main.tstep_panel[panelselect-1]
        time = self.main.taxis[tstep-1]
        aspect = self.main.aspect_panel[panelselect-1]

        figure.clear()

        interpolation = 'nearest'

        fontmax = 10
        barmax = 0.12
        matplotlib.rc('xtick', labelsize=fontmax)
        matplotlib.rc('ytick', labelsize=fontmax)
        fontsize = fontmax
        cbarwidth = barmax

        title = species+' '+phase[0]+'-'+phase[1]

        xtitle = r'z ($\mu$m)'; ytitle = r'x ($\mu$m)'
        nbin = 300

        if self.main.dim == 2:
            local = local[0]

        ax1 = figure.add_subplot(111)
        #self.plot.cla()

        #if len(self.main.pdata_container[(species,'w',tstep)]) > 0 :
        if len(local) > 1:

            ###################
            # x-axis
            ###################
            if phase[1] in ['px','py','pz']:
                p1min = np.min(self.main.pdata_container[(species,phase[1],tstep)][local])
                p1max = np.max(self.main.pdata_container[(species,phase[1],tstep)][local])
                xtitle = r'%s ($c$)'%(phase[1])
                # if the minimunm and maximum values are the same, 
                #   an error occurs in the histogram.
            elif phase[1] in ['ene']:
                p1min = np.min(self.main.pdata_container[(species,phase[1],tstep)][local])
                p1max = np.max(self.main.pdata_container[(species,phase[1],tstep)][local])
                xtitle = r'%s ($\gamma$-1)'%(phase[1])
            elif phase[1] in ['x','y','z']:
                p1min = x1min
                p1max = x1max
                xtitle = r'%s ($\mu$m)'%(phase[1])
            elif phase[1] in ['loglin', 'loglog']:
                p1min = np.min(self.main.pdata_container[(species,'ene',tstep)][local])
                p1max = np.max(self.main.pdata_container[(species,'ene',tstep)][local])
                xtitle = r'%s ($\gamma$-1)'%('ene')
       
            ###################
            # y-axis
            ###################
            if phase[0] in ['px','py','pz']:
                p2min = np.min(self.main.pdata_container[(species,phase[0],tstep)][local])
                p2max = np.max(self.main.pdata_container[(species,phase[0],tstep)][local])
                ytitle = r'%s ($c$)'%(phase[0])
            elif phase[0] in ['ene']:
                p2min = np.min(self.main.pdata_container[(species,phase[0],tstep)][local])
                p2max = np.max(self.main.pdata_container[(species,phase[0],tstep)][local])
                ytitle = r'%s ($\gamma$-1)'%(phase[0])
            elif phase[0] in ['x','y','z']:
                p2min = x2min
                p2max = x2max
                ytitle = r'%s ($\mu$m)'%(phase[0])
            elif phase[0] in ['fE']:
                ytitle = 'f(E)'
            
            
            if p1min == p1max:
                if p1min != 0:
                    p1min = p1min*.5
                    p1max = p1min*3.
                else:
                    p1max = 1.0

            if phase[0] != 'fE':  
                if p2min == p2max:
                    if p2min != 0:
                        p2min = p2min*.5
                        p2max = p2min*3.
                    else:
                        p2max = 1.0

            if phase[0] != 'fE':

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

            elif phase[1] == 'loglin':

                nbin = 200
                eaxis = p1min+np.arange(nbin)*(p1max-p1min)/nbin
            
                histogram_1d=histogram_cic_1d(self.main.pdata_container[(species,'ene',tstep)][local], 
                        self.main.pdata_container[(species,'w',tstep)][local], nbin, p1min , p1max )
                ax1.semilogy(eaxis, histogram_1d)
                ax1.axes.set_xlim([p1min,p1max])
                ax1.set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                ax1.set_xlabel(xtitle, fontsize=fontsize)
                ax1.set_ylabel(ytitle, fontsize=fontsize)

            elif phase[1] == 'loglog':

                nbin = 200
                values, bins = np.histogram(self.main.pdata_container[(species,'ene',tstep)][local], 
                        bins=nbin, normed=True, weights= self.main.pdata_container[(species,'w',tstep)][local])
                vmin = np.min(values); vmax = np.max(values)   
                
                ax1.loglog(bins[:-1], values)
                ax1.axes.set_xlim([1.e-2,p1max])
                ax1.set_title(title+'  (%6.1f fs)'%(time), x=0.3, fontsize=fontsize)
                ax1.set_xlabel(xtitle, fontsize=fontsize)
                ax1.set_ylabel(ytitle, fontsize=fontsize)
                


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

    
        #if nrow < 4 or ncolumn < 4:
        ax1.axes.get_figure().tight_layout()


