import numpy as np

from picviewer.controller.panel_controller import PanelController
from picviewer.dataloader.data_collector import DataCollector
from picviewer.dataplotter.prepare_plot import PreparePlot
from picviewer.dataplotter.prepare_localplot import PrepareLocalPlot

import matplotlib.patches as patches

class MouseController():
    """
        mouse control class
        
    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow

        self.main.canvas.mpl_connect('motion_notify_event', self.motion_notify)
        self.main.canvas.mpl_connect('button_press_event', self.onclick)
        self.main.canvas.mpl_connect('button_release_event', self.release_click)


        self.panelcontroller = PanelController(self.main)
        
        # Data collect class
        self.collectdata = DataCollector(self.main)
        # Plot class
        self.prepareplot = PreparePlot(self.main)

        self.preparelocalplot = PrepareLocalPlot(self.main)
    
        self.main.pressed= False

        # local selection variables in each panel
        self.main.resize = np.arange(self.main.nrow*self.main.ncolumn)
        self.main.translate = np.arange(self.main.nrow*self.main.ncolumn)
        self.main.xc = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.yc = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.xcenter = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.ycenter = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.rectw = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.recth = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.xini = np.zeros(self.main.nrow*self.main.ncolumn)
        self.main.yini = np.zeros(self.main.nrow*self.main.ncolumn)

        # selection tool
        self.main.resize[:] = 0  
            # 0: size increase from beginning
            # 1: direction resize
            # 2: waiting
        self.main.translate[:] = 0

        # subpanel window
        self.main.subplot = {}
        self.main.subaxes = {}
        self.main.subcbars = {}

        

    def motion_notify(self,event):
        """
        mouse in motion
        """
        if not event.inaxes in self.main.axes.values(): return
        self.main.x_m, self.main.y_m = event.xdata, event.ydata
        self.main.coordLabel.setText("(x1,x2)=(%4.2f, %4.2f)" %(self.main.x_m, self.main.y_m)) 

        ############################################################
        # Local selection tool
        ############################################################ 
        # self.main.xc[panelselect-1]       --> x-center of rectangle (varying)
        # self.main.yc[panelselect-1]       --> y-center of rectangle (varying)
        # self.main.xcenter[panelselect-1]  --> x-center of rectangle (after mouse release)
        # self.main.ycenter[panelselect-1]  --> y-center of rectangle (after mouse release)
        # self.main.xini[panelselect-1]     --> left edge of rectangle (after mouse release)
        # self.main.yini[panelselect-1]     --> left edge of rectangle (after mouse release)
        # self.main.rectw[panelselect-1]     --> width of rectangle
        # self.main.recth[panelselect-1]     --> height of rectangle
        ############################################################ 
        if self.main.rectangleCheckBox.isChecked():
            if not self.main.toolbar.actions()[4].isChecked() and not self.main.toolbar.actions()[5].isChecked():

                if self.main.pressed:

                    panelselect = self.main.panelselect

                    # increase rectangle size from beginning
                    if self.main.resize[panelselect-1] == 0:

                        self.main.rectw[panelselect-1] = self.main.x_m - self.main.x_o
                        self.main.recth[panelselect-1] = self.main.y_m - self.main.y_o
                        self.main.xc[panelselect-1] = self.main.x_o+self.main.rectw[panelselect-1]*.5
                        self.main.yc[panelselect-1] = self.main.y_o+self.main.recth[panelselect-1]*.5

                        rect = patches.Rectangle((self.main.x_o, self.main.y_o),self.main.rectw[panelselect-1], self.main.recth[panelselect-1],
                            linewidth=0.8,edgecolor='black',facecolor='none')

                        [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]

                        self.main.axes[panelselect-1].add_patch(rect)
                        self.main.canvas.draw_idle()

                    elif self.main.resize[panelselect-1] == 1:  # resize

                        self.main.rectw[panelselect-1] = self.main.x_m - self.main.xini[panelselect-1]
                        self.main.recth[panelselect-1] = self.main.y_m - self.main.yini[panelselect-1]
                        self.main.xc[panelselect-1] = self.main.xini[panelselect-1]+self.main.rectw[panelselect-1]*.5
                        self.main.yc[panelselect-1] = self.main.yini[panelselect-1]+self.main.recth[panelselect-1]*.5
            
                        #circ = patches.Circle((xcenter,ycenter), 1,facecolor='none',edgecolor='r')
                        rect = patches.Rectangle((self.main.xini[panelselect-1], 
                                self.main.yini[panelselect-1]),self.main.rectw[panelselect-1], 
                                self.main.recth[panelselect-1],
                            linewidth=0.8,edgecolor='black',facecolor='none')

                        [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]

                        self.main.axes[panelselect-1].add_patch(rect)
                        #self.axes[1].add_patch(circ)
                        self.main.canvas.draw_idle()

                    #elif self.main.resize == 2: # horizontal resize
                    #
                    #    self.main.rectw = self.main.x_m - self.main.xini
                    #    self.main.recth = abs(self.main.recth)
                    #
                    #    self.main.xc = self.main.xini+self.main.rectw*.5
                    #
                    #    rect = patches.Rectangle((self.main.xini, self.main.yini),self.main.rectw, self.main.recth,
                    #        linewidth=0.8,edgecolor='black',facecolor='none')
                    #
                    #    [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]
                    #
                    #   self.main.axes[panelselect-1].add_patch(rect)
                    #    #self.axes[1].add_patch(circ)
                    #    self.main.canvas.draw_idle()
                    #
                    #elif self.main.resize == 3: # vertical resize
                    #
                    #    self.main.rectw = abs(self.main.rectw)
                    #    self.main.recth = self.main.y_m - self.main.yini
                    #
                    #    self.main.yc = self.main.yini+self.main.recth*.5
                    #
                    #    rect = patches.Rectangle((self.main.xini, self.main.yini),self.main.rectw, self.main.recth,
                    #        linewidth=0.8,edgecolor='black',facecolor='none')
                    #    
                    #    [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]
                    #
                    #    self.main.axes[panelselect-1].add_patch(rect)
                    #    #self.axes[1].add_patch(circ)
                    #    self.main.canvas.draw_idle()
                    
                    elif self.main.translate[panelselect-1] == 1: # translate

                        xtrans = self.main.x_m - self.main.x_o
                        ytrans = self.main.y_m - self.main.y_o

                        self.main.xc[panelselect-1] = self.main.xcenter[panelselect-1] + xtrans
                        self.main.yc[panelselect-1] = self.main.ycenter[panelselect-1] + ytrans
                        
                        #circ = patches.Circle((xc,yc), 1,facecolor='none',edgecolor='r')
                        rect = patches.Rectangle((self.main.xc[panelselect-1]-self.main.rectw[panelselect-1]*.5, 
                                    self.main.yc[panelselect-1]-self.main.recth[panelselect-1]*.5),
                                    self.main.rectw[panelselect-1],self.main.recth[panelselect-1],
                                linewidth=0.8,edgecolor='black',facecolor='none')

                        [p.remove() for p in reversed(self.main.axes[panelselect-1].patches)]

                        self.main.axes[panelselect-1].add_patch(rect)
                        #self.axes[1].add_patch(circ)
                        self.main.canvas.draw_idle()

   
    def onclick(self, event):
        """
        mouse pressed
        """
        # return if mouse click is outside panels
        if not event.inaxes in self.main.axes.values(): return

        self.main.pressed = True  # True if mouse is on-click
        # Select a panel by mouse clicking
        self.main.panelselect = np.where(np.array(self.main.axes.values()) == event.inaxes)[0][0]+1
    
        # panel button matrix: i: row, j: column
        i = (self.main.panelselect-1)/self.main.ncolumn
        j = np.mod((self.main.panelselect-1),self.main.ncolumn)
        self.main.panelbuttons[(i,j)].setChecked(True)
        self.panelcontroller.panelbutton()

        self.main.x_o, self.main.y_o = event.xdata, event.ydata
        
        ############################################################
        # Local selection tool
        ############################################################
        if self.main.rectangleCheckBox.isChecked():
            if not self.main.toolbar.actions()[4].isChecked() and not self.main.toolbar.actions()[5].isChecked():

                panelselect = self.main.panelselect

                if self.main.resize[panelselect-1] == 2:
                    # selection error
                    epsilon = 3./100
                    x1min = float(self.main.x1minLabel.text())
                    x1max = float(self.main.x1maxLabel.text())
                    x2min = float(self.main.x2minLabel.text())
                    x2max = float(self.main.x2maxLabel.text())
                    
                    xedges = np.array([self.main.xcenter[panelselect-1] - self.main.rectw[panelselect-1]*.5, 
                                    self.main.xcenter[panelselect-1] + self.main.rectw[panelselect-1]*.5, 
                                    self.main.xcenter[panelselect-1] + self.main.rectw[panelselect-1]*.5, 
                                    self.main.xcenter[panelselect-1] - self.main.rectw[panelselect-1]*.5])

                    yedges = np.array([self.main.ycenter[panelselect-1] - self.main.recth[panelselect-1]*.5, 
                                    self.main.ycenter[panelselect-1] - self.main.recth[panelselect-1]*.5, 
                                    self.main.ycenter[panelselect-1] + self.main.recth[panelselect-1]*.5, 
                                    self.main.ycenter[panelselect-1] + self.main.recth[panelselect-1]*.5])
                    d = np.hypot(xedges - self.main.x_o, yedges- self.main.y_o)
                    indseq, = np.nonzero(d == d.min())
                    ind = indseq[0]
                    if d[ind] < epsilon*np.mean([np.abs(x1max-x1min), np.abs(x2max-x2min)]):

                        self.main.resize[panelselect-1] = 1 # all direction resize

                        self.main.xini[panelselect-1] = xedges[np.mod(ind+2,4)]
                        self.main.yini[panelselect-1] = yedges[np.mod(ind+2,4)]
                    
                    #elif self.main.y_o > np.min(yedges) and self.main.y_o < np.max(yedges):
                    #    xedges = np.array([self.main.xcenter - self.main.rectw*.5, 
                    #                self.main.xcenter + self.main.rectw*.5])
                    #    d = abs(xedges - self.main.x_o)
                    #    indseq, = np.nonzero(d == d.min())
                    #    ind = indseq[0]
                    #    if d[ind] < 1*epsilon*np.abs(x1max-x1min):
                    #
                    #         self.main.resize = 2 # horizontal resize
                    #
                    #        self.main.xini = xedges[np.mod(ind+1,2)]
                    #        self.main.yini = np.min(yedges)

                    #elif self.main.x_o > np.min(xedges) and self.main.x_o < np.max(xedges):
                    #    yedges = np.array([self.main.ycenter - self.main.recth*.5, 
                    #                self.main.ycenter + self.main.recth*.5])
                    #    d = abs(yedges - self.main.y_o)
                    #    indseq, = np.nonzero(d == d.min())
                    #    ind = indseq[0]
                    #    if d[ind] < 3*epsilon*np.abs(x2max-x2min):
                    #
                    #        self.main.resize = 3 # vertical resize

                    #        self.main.xini = np.min(xedges)
                    #        self.main.yini = yedges[np.mod(ind+1,2)]

                    elif self.main.x_o > np.min(xedges) and self.main.x_o < np.max(xedges) \
                        and self.main.y_o > np.min(yedges) and self.main.y_o < np.max(yedges):

                        self.main.translate[panelselect-1] = 1    # translate

                    elif not (self.main.x_o > np.min(xedges) and self.main.x_o < np.max(xedges) \
                        and self.main.y_o > np.min(yedges) and self.main.y_o < np.max(yedges)):

                        self.main.resize[panelselect-1] = 0    # new rectangle


    def release_click(self, event):
        """
        mouse released

        """
        
        # Return if mouse click is outside the panel.
        if not event.inaxes in self.main.axes.values(): return
        # Return if mouse is released inside panel but pressed outside.
        if not self.main.pressed: return
        
        # QtGui.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

        # If mouse is pressed and released at the same position, pick a data point and return
        self.main.x_r, self.main.y_r = event.xdata, event.ydata    
        if self.main.x_r == self.main.x_o and self.main.y_r == self.main.y_o: 
            
            if self.main.field_select_panel[self.main.panelselect-1]:
                tstep = self.main.tstep_panel[self.main.panelselect-1]
                zvalue = self.PickingValue(self.main.x_r, self.main.y_r)
               
                self.main.coordLabelVal.setText("(x1,x2,Val)=(%4.1f, %4.1f, %4.1e)" %(self.main.x_r, self.main.y_r, zvalue)) 

            self.main.pressed = False
            return

        panelselect = self.main.panelselect

        #  if the zoom-in button in the Navigation toolbar is on
        if self.main.toolbar.actions()[5].isChecked():  

            tstep = self.main.tstep_panel[panelselect-1]

            if self.main.dim == 3:

                if self.main.sliceplane_panel[self.main.panelselect-1] == 'yx':
                    x1axis = self.main.xaxis_dic[tstep-1]
                    x2axis = self.main.yaxis_dic[tstep-1]
                if self.main.sliceplane_panel[self.main.panelselect-1] == 'xz':
                    x1axis = self.main.zaxis_dic[tstep-1]
                    x2axis = self.main.xaxis_dic[tstep-1]
                if self.main.sliceplane_panel[self.main.panelselect-1] == 'yz':
                    x1axis = self.main.zaxis_dic[tstep-1]
                    x2axis = self.main.yaxis_dic[tstep-1]
            else:
                x1axis = self.main.zaxis_dic[tstep-1]
                x2axis = self.main.xaxis_dic[tstep-1]

            # Do not zoom in but return if mouse is pressed and released at very close points. 
            # This might be a mistake of clicking rather than intending to drag.
            #if abs(self.main.x_r -self.main.x_o)/(x1axis[-1]-x1axis[0]) < 0.03 and \
            #        abs(self.main.y_r -self.main.y_o)/(x1axis[-1]-x1axis[0]) < 0.03: 
            #    self.main.pressed = False
            #    return

            # Change the space sliders
            x1minloc = int((np.min([self.main.x_o,self.main.x_r])-x1axis[0])/(x1axis[-1]-x1axis[0])*100.)
            x1maxloc = int((np.max([self.main.x_o,self.main.x_r])-x1axis[0])/(x1axis[-1]-x1axis[0])*100.)
            x2minloc = int((np.min([self.main.y_o,self.main.y_r])-x2axis[0])/(x2axis[-1]-x2axis[0])*100.)
            x2maxloc = int((np.max([self.main.y_o,self.main.y_r])-x2axis[0])/(x2axis[-1]-x2axis[0])*100.)
            
            # slider value changed ---> call SpaceController class
            self.main.x1minSlider.setValue(x1minloc)
            self.main.x1maxSlider.setValue(x1maxloc)
            self.main.x2minSlider.setValue(x2minloc)
            self.main.x2maxSlider.setValue(x2maxloc)

            # Do not call makeplot function!
            # The Matplotlib Navigatorn has a re-plot function internally to avoid plotting twice.
            

        self.main.pressed = False

        ############################################################
        # Local selection tool
        ############################################################
        if self.main.rectangleCheckBox.isChecked():
            if not self.main.toolbar.actions()[4].isChecked() and not self.main.toolbar.actions()[5].isChecked():

                self.main.translate[panelselect-1] = 0
                self.main.resize[panelselect-1] = 2   # waiting response 
                #global xcenter, ycenter
                self.main.xcenter[panelselect-1] = self.main.xc[panelselect-1]
                self.main.ycenter[panelselect-1] = self.main.yc[panelselect-1]

                # Here make a local plot
                self.main.x1localmin= self.main.xc[panelselect-1] - abs(self.main.rectw[panelselect-1])*.5
                self.main.x1localmax= self.main.xc[panelselect-1] + abs(self.main.rectw[panelselect-1])*.5
                self.main.x2localmin= self.main.yc[panelselect-1] - abs(self.main.recth[panelselect-1])*.5
                self.main.x2localmax= self.main.yc[panelselect-1]+ abs(self.main.recth[panelselect-1])*.5

                # avoid error when the area of the rectangle is too small
                # this might be a mistake of just clicking

                x1min = float(self.main.x1minLabel.text())
                x1max = float(self.main.x1maxLabel.text())
                x2min = float(self.main.x2minLabel.text())
                x2max = float(self.main.x2maxLabel.text())

            
                epsilon = 0.0002
                if (self.main.x1localmax-self.main.x1localmin)*(self.main.x2localmax-self.main.x2localmin) \
                     > epsilon*(x1max-x1min)*(x2max-x2min):

                    if self.main.field_select_panel[panelselect-1]:
                        self.preparelocalplot.plotfield()
                    else:
                        self.preparelocalplot.plotparticle()


    def PickingValue(self, x1, x2):

        panelselect = self.main.panelselect
        tstep = self.main.tstep_panel[panelselect-1]
        xaxis = self.main.xaxis_dic[tstep-1]
        yaxis = self.main.yaxis_dic[tstep-1]
        zaxis = self.main.zaxis_dic[tstep-1]
        field = self.main.field_panel[panelselect-1]
        amrlevel = self.main.amrlevel_panel[panelselect-1]
        

        if self.main.dim == 2:
            iloc = np.where(zaxis > x1)[0][0]
            jloc = np.where(xaxis > x2)[0][0]
            zvalue = self.main.fdata_container[(field,tstep,amrlevel)][jloc, iloc]
            
        else:   # 3D
            if self.main.sliceplane_panel[panelselect-1] == 'yx':
                iloc = np.where(xaxis > x1)[0][0]
                jloc = np.where(yaxis > x2)[0][0]
                kloc = int(1.0*len(zaxis)*self.main.slicevalue_panel[panelselect-1]/30)
                
            if self.main.sliceplane_panel[panelselect-1] == 'xz':
                iloc = np.where(xaxis > x2)[0][0]
                kloc = np.where(zaxis > x1)[0][0]
                jloc = int(1.0*len(yaxis)*self.main.slicevalue_panel[panelselect-1]/30)

            if self.main.sliceplane_panel[panelselect-1] == 'yz':
                jloc = np.where(yaxis > x2)[0][0]
                kloc = np.where(zaxis > x1)[0][0]
                iloc = int(1.0*len(xaxis)*self.main.slicevalue_panel[panelselect-1]/30)

            zvalue = self.main.fdata_container[(field,tstep,amrlevel)][iloc, jloc, kloc]

        return zvalue

