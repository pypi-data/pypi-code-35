'''
Created on Aug 17, 2018

@author: reynolds
'''

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QFrame, QWidget,QApplication, QPushButton, QLabel
from PyQt5.Qt import QLineEdit
from wrtdk.data.state.state import state
from wrtdk.qt5.animations import CubeWidget
from wrtdk.qt5.plots import PlotParameters, Plot2DWidget, Plot3DWidget

import sys, random
import numpy as np
from wrtdk.qt5.widgets import SoftwareLED

class LogWidget(QWidget):
    ''' a widget for logging collected data '''
    
    def __init__(self,parent=None,default='',lfnt=None,tfnt=None,align=None):
        ''' constructor '''
        QWidget.__init__(self,parent)
        
        # define widgets
        self.txt = self._get_qlineedit('',tfnt,align)
        self.log = self._get_qpushbutton('LOG',lfnt,align)
        self.log.setStyleSheet('background-color: green')
        
        # layout widgets
        l = QGridLayout()
        l.addWidget(self.txt,0,0,1,1)
        l.addWidget(self.log,0,1,1,1)
        l.setColumnStretch(0,2)
        self.setLayout(l)
        
        # define state variables
        self._log = False
        
    def _get_qlineedit(self,txt='',fnt=None,align=None):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if fnt is not None: l.setFont(fnt)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qpushbutton(self,txt='',fnt=None,align=None):
        ''' creates a qpush button '''
        b = QPushButton(txt)
        if fnt is not None: b.setFont(fnt)
        if align is not None: b.setAlignment(align)
        return b
        
    def setEnabled(self,enabled=False):
        ''' sets the enabled state of the logger '''
        self.log.setEnabled(enabled)
        self.txt.setReadOnly(not enabled)
        
    def isLogging(self):
        ''' returns whether the widget is in log mode or not '''
        return self._log

    def setStarted(self):
        ''' sets the widget in logging mode '''
        self.log.setStyleSheet('background-color: red')
        self.log.setText('STOP')
        self._log = True

    def setStopped(self):
        ''' sets the widget in not logging mode '''
        self.log.setStyleSheet('background-color: green')
        self.log.setText('LOG')
        self._log = False

    def getFilename(self):
        ''' returns the current filename '''
        return self.txt.text()

class GPGGAWidget(QFrame):
    ''' a widget for displaying the GPGGA information '''
    def __init__(self,parent=None,rtk=False,lfnt=None,
                 tfnt=None,align=None,frame=QFrame.StyledPanel | QFrame.Plain):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # create the widgets
        self._time = self._get_qlineedit(tfnt,align)
        self._lat = self._get_qlineedit(tfnt,align)
        self._lon = self._get_qlineedit(tfnt,align)
        self._fix = self._get_qlineedit(tfnt,align)
        self._n = self._get_qlineedit(tfnt,align)
        self._dop = self._get_qlineedit(tfnt,align)
        
        #setup the ui
        l = QGridLayout()
        l.addWidget(self._get_qlabel('UTC Time',lfnt,align),0,0,1,1)
        l.addWidget(self._get_qlabel('Latitude',lfnt,align),0,1,1,1)
        l.addWidget(self._get_qlabel('Longitude',lfnt,align),0,2,1,1)
        l.addWidget(self._get_qlabel('N Sats',lfnt,align),0,3,1,1)
        l.addWidget(self._get_qlabel('Quality',lfnt,align),0,4,1,1)
        l.addWidget(self._get_qlabel('DOP',lfnt,align),0,5,1,1)
        l.addWidget(self._time,1,0,1,1)
        l.addWidget(self._lat,1,1,1,1)
        l.addWidget(self._lon,1,2,1,1)
        l.addWidget(self._fix,1,3,1,1)
        l.addWidget(self._n,1,4,1,1)
        l.addWidget(self._dop,1,5,1,1)
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(frame)
        
        # initialize state variables
        self._dop_state = state()
        self._fix_state = state()
        self._rtk = rtk
        
    def set_data(self,time='',lat=360,lon=360,n=0,fix=0,dop=np.NaN):
        ''' sets the data on the plot and appends to the map '''
        self._time.setText(time)
        self._lat.setText('%.6f'%lat)
        self._lon.setText('%.6f'%lon)
        self._n.setText('%d'%n)
        self._set_fix(fix)
        self._set_dop(dop)
        
    def clear(self):
        ''' reset all the text boxes '''
        self._time.setText('')
        self._lat.setText('')
        self._lon.setText('')
        self._n.setText('')
        self._fix.setText('')
        self._fix.setStyleSheet('')
        self._dop.setText('')
        self._dop.setStyleSheet('')
        
    def _set_fix(self,fix=1):
        ''' sets the fix of the gnss receiver '''
        
        if not self._fix_state.isDifferent(fix): return
        
        self._fix.setText('%d'%fix)# update the text
        if self._rtk:
            if fix == 4: self._fix.setStyleSheet('background-color: green')
            else: self._fix.setStyleSheet('background-color: red')
            
    def _set_dop(self,dop=100):
        ''' sets the dop text and warning '''
        if not self._dop_state.isDifferent(dop): return
        
        self._dop.setText('%.2f' % dop)# update the text
        if not self._rtk:
            if dop >= 2: self._dop.setStyleSheet('background-color: red')
            else: self._dop.setStyleSheet('background-color: green')
        
    def _get_qlabel(self,text,fnt,algn):
        ''' creates the labels '''
        l = QLabel(text)
        if fnt is not None: l.setFont(fnt)
        if algn is not None: l.setAlignment(algn)
        return l
        
    def _get_qlineedit(self,fnt,algn):
        ''' creates the line edits '''
        le = QLineEdit()
        le.setReadOnly(True)
        if fnt is not None: le.setFont(fnt)
        if algn is not None: le.setAlignment(algn)
        return le

class IMUVisualWidget(QFrame):
    
    def __init__(self,parent=None,px=.2,py=.2,pz=.2,tfnt=None):
        QFrame.__init__(self,parent)
        self.roll = self._get_txt('Roll:',tfnt)
        self.pitch = self._get_txt('Pitch:',tfnt)
        self.yaw = self._get_txt('Yaw:',tfnt)
        self.imu = CubeWidget(self,px=px,py=py,pz=pz)
        
        l = QGridLayout()
        l.addWidget(self.imu,0,0,1,3)
        l.addWidget(self.roll,1,0,1,1)
        l.addWidget(self.pitch,1,1,1,1)
        l.addWidget(self.yaw,1,2,1,1)
        
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def _get_txt(self,text='',fnt=None):
        txt = QLineEdit(text)
        txt.setReadOnly(True)
        if fnt is not None: txt.setFont(fnt)
        return txt
    
    def setEuler(self,roll,pitch,yaw):
        self.roll.setText('Roll: %.2f' % roll)
        self.pitch.setText('Pitch: %.2f' % pitch)
        self.yaw.setText('Yaw: %.2f' % yaw)
        self.imu.update(roll,pitch,yaw)
        
    def clear(self):
        ''' clears the IMU widget '''
        self.setEuler(0,0,0)
        
class GCSMapWidget(QFrame):
    ''' a class for a GCS map '''
    
    def __init__(self,parent=None,lines=1,leg=['Path'],lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # setup the plot
        self.plot = Plot2DWidget(self,
                                 parameters=PlotParameters('GCS Map',
                                                           'Longitude (deg)',
                                                           'Latitude (deg)',
                                                           lsize=lsize,
                                                           tsize=tsize),
                                 lines=lines)
        self.plot.axes.set_aspect('equal')
        self.plot.set_linestyle(line=0,style='None')
        self.plot.set_marker(line=0,marker='s')
        self.plot.set_legend(leg)
        
        #layout the map
        l = QGridLayout()
        l.setSpacing(0)
        l.addWidget(self.plot)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet('background-color: white')
        
    def append(self,x=0,y=0,line=0):
        ''' appends to the plot data '''
        self.plot.append(x,
                         y,
                         line,
                         autoscale=True)

class UTMMapWidget(QFrame):
    ''' a class for a UTM map '''
    
    def __init__(self,parent=None,lines=1,leg=['Path'],lsize=10,tsize=16,xref=0,yref=0):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # setup the reference coordinates
        self._x_ref = xref
        self._y_ref = yref
        
        # setup the plot
        parameters = PlotParameters('UTM Map',
                                    'Easting - %.2f (m)' % self._x_ref,
                                    'Northing - %.2f (m)' % self._y_ref,
                                    lsize=lsize,
                                    tsize=tsize)
        self.plot = Plot2DWidget(parent=self,parameters=parameters,lines=lines)
        self.plot.axes.set_aspect('equal')
        self.plot.set_linestyle(line=0,style='None')
        self.plot.set_marker(line=0,marker='s')
        self.plot.set_legend(leg)
        
        #layout the map
        l = QGridLayout()
        l.setSpacing(0)
        l.addWidget(self.plot)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet('background-color: white')
        
    def setReference(self,x=0,y=0):
        ''' sets the reference coordinates '''
        self._x_ref = x
        self._y_ref = y
        self.plot.axes.set_xlabel('Easting - %.2f (m)' % self._x_ref)
        self.plot.axes.set_xlabel('Northing - %.2f (m)' % self._y_ref)
        
    def append(self,x=0,y=0,line=0):
        ''' appends to the plot '''
        self.plot.append(x-self._x_ref,
                         y-self._x_ref,
                         line,
                         autoscale=True)

class GPGGAVisualWidget(QFrame):
    ''' a class for visually displaying the NMEA string '''
    
    def __init__(self,parent=None,rtk=False,lfnt=None,tfnt=None,align=None,
                 lsize=10,tsize=16):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        # create the widgets
        self._gga = GPGGAWidget(self,rtk=rtk,
                                tfnt=tfnt,lfnt=lfnt,
                                align=align,frame=QFrame.Plain)
        self._map = GCSMapWidget(self,lsize=lsize,tsize=tsize)# map widget
        
        #setup the ui
        l = QGridLayout()
        l.addWidget(self._gga)
        l.addWidget(self._map,2,0,6,6)
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        # initialize state variables
        self._dop_state = state()
        self._fix_state = state()
        self._rtk = rtk
        
    def set_data(self,time='',lat=360,lon=360,n=0,fix=0,dop=np.NaN,append=True):
        ''' sets the data on the plot and appends to the map '''
        self._gga.set_data(time, lat, lon, n, fix, dop)
        if append: self._map.append(lon,lat)
    
class RTMagWidget(QFrame):
    
    def __init__(self,parent=None,lsize=10,tsize=16):
        QFrame.__init__(self,parent)
        
        self.det = SoftwareLED(self,'DETECTION')
        _curr_m = self._get_qlabel(txt='Current Moment:')
        self.curr_m = self._get_qlineedit(readonly=True)
        _track_m = self._get_qlabel(txt='Track Moment:')
        self.track_m = self._get_qlineedit(readonly=True)
        _source_n = self._get_qlabel(txt='Total Sources:')
        self.source_n = self._get_qlineedit(readonly=True)
        
        self.plot = Plot3DWidget(parameters=
                                 PlotParameters(xlabel='x(m)',
                                                ylabel='y(m)',
                                                zlabel='z(m)',
                                                lsize=lsize,
                                                tsize=tsize),
                                 lines=0)
        self.plot.add_line([], [], [],'ko-')
        self.plot.add_line([],[],[],'bx',markersize=14,markeredgewidth=8)
        self.plot.add_line([], [], [],'mo-')
        self.plot.set_legend(['Path','Track','Source'])
        
        l = QGridLayout()
        l.addWidget(self.det,0,0,1,1)
        l.addWidget(_curr_m,0,1,1,1)
        l.addWidget(self.curr_m,0,2,1,1)
        l.addWidget(_source_n,0,3,1,1)
        l.addWidget(self.source_n,0,4,1,1)
        l.addWidget(_track_m,0,5,1,1)
        l.addWidget(self.track_m,0,6,1,1)
        l.addWidget(self.plot,1,0,1,7)
        
        l.setSpacing(2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
    def _get_qlabel(self,txt='',font=None,align=None):
        ''' creates the qlabels '''
        l = QLabel(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qlineedit(self,txt='',font=None,align=None,readonly=False):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        l.setReadOnly(readonly)
        return l
    
    def clear(self):
        ''' clears all the plots, text boxes and software LEDs '''
        for i in range(self.plot.line_total()-1,2,-1):self.plot.remove_line(i)
        self.plot.clear_line(0)
        self.plot.clear_line(1)
        self.curr_m.setText('')
        self.source_n.setText('')
        self.track_m.setText('')
        self.det.reset()
    
    def appendPath(self,x,y,z):
        ''' appends to the path line '''
        self.plot.append(x,y,z,line=0,autoscale=True)
        
    def appendTrack(self,x,y,z):
        ''' appends to the mean inversion locations '''
        self.plot.append(x,y,z,line=1,autoscale=True)
        
    def addSource(self,x,y,z):
        ''' adds an inversion line '''
        self.plot.add_line(x,y,z,'mo-')
        
    def setTrackMoment(self,m=-1):
        ''' sets the track moment '''
        self.track_m.setText('%.2f A m 2' % m)
        
    def setCurrentMoment(self,m=-1):
        ''' sets the current moment '''
        self.curr_m.setText('%.2f A m^2' % m)
        
    def setTotalSources(self,n=-1):
        self.source_n.setText('%d' % n)
        
    def setDetection(self,detection=False):
        ''' sets the detection state '''
        if detection: self.det.setBad()
        else: self.det.reset()
        
class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = LogWidget(self)
        clear = QPushButton('CLEAR')
        clear.clicked.connect(self._clear)
        self.nmea = GPGGAWidget(self)
        self.imu = IMUVisualWidget(self)
        self.map = GPGGAVisualWidget(self,
                                     rtk=True,
                                     align=QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter,
                                     lsize=10,
                                     tsize=16)
        self.utm = UTMMapWidget(self,lsize=10,tsize=16)
        self.gcs = GCSMapWidget(self,lsize=10,tsize=16)
        self.rtmag = RTMagWidget(self)
        layout = QGridLayout()
        layout.addWidget(self.w,0,0,1,2)
        layout.addWidget(clear,0,2,1,1)
        layout.addWidget(self.nmea,1,0,1,3)
        layout.addWidget(self.imu,2,0,1,1)
        layout.addWidget(self.map,2,1,1,1)
        layout.addWidget(self.utm,2,2,1,1)
        layout.addWidget(self.gcs,3,0,1,1)
        layout.addWidget(self.rtmag,3,2,1,1)
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        self.setLayout(layout)
        
        self.w.log.clicked.connect(self.onClick)
        
        self._det = False
        
    def _clear(self):
        ''' clears the real time plot '''
        self.rtmag.clear()
        
    def onClick(self):
        if self.w.isLogging(): 
            self.w.setStopped()
        else:
            print('filename: %s.dat'%self.w.getFilename())
            self.w.setStarted()
        
        self.map.set_data('1234',43.0,127.4,3,12,100)
        self.nmea.set_data('1234',43.0,127.4,3,8,100)
        
        #test utm
        self.utm.plot.set_data([1,2,3,4],[1,1,1,1],autoscale=True)
        self.utm.plot.append(5,3,autoscale=True)
        
        # test gcs
        self.gcs.append(0,2,line=0)
        self.gcs.append(1,2,line=0)
        
        self.rtmag.appendPath([random.random()],
                                    [random.random()],
                                    [random.random()])
        
        self.rtmag.appendTrack([random.random()],
                                    [random.random()],
                                    [random.random()])
        
        self.rtmag.addSource([0,random.random()],
                                    [0,random.random()],
                                    [0,random.random()])
        
        self.rtmag.setTrackMoment(random.random())
        self.rtmag.setCurrentMoment(random.random())
        self.rtmag.setTotalSources(random.randint(0,100))
        
        self.rtmag.setDetection(self._det)
        self._det = not self._det
    
if __name__.startswith('__main__'):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Color Picker Demo")
    window.show()
    app.exec_()