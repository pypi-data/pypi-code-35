#-------------------------------------------------------------------------------
# Name:        PIDCtrlModelWindow
# Purpose:
#
# Author:      elbar
#
# Created:     09/11/2012
# Copyright:   (c) elbar 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sip # Ugly HACK
sip.setapi("QString",2)
sip.setapi("QVariant",2)
sip.setapi("QDate",2)
sip.setapi("QDateTime",2)
sip.setapi("QTime",2)
sip.setapi("QTextStream",2)
sip.setapi("QUrl",2)

from PyQt4 import QtGui, QtCore
import sys, os
import logging

from Ui_pid_tune_methods_main_window import Ui_MainWindow

import Utils
import PIDRecipe
import PlotWidget as plt
import ControlSys  as ctrl

from PIDTuneMethodsAbout import PIDTuneMethodsAboutWindow

#-------------------------------------------------------------------------------
class PIDTuneMethodsWindow(QtGui.QMainWindow):
    """ Class wrapper for about window ui """

    def __init__(self):
        super(PIDTuneMethodsWindow,self).__init__()
        # init
        # process params
        self.gain = 0.0
        self.tau = 0.0
        self.dead_time = 0.0
        # PID params
        self.lambda_tau = 0.0
        self.lambda_tau_ratio = 0.0
        self.kc = 0.0
        self.ti = 0.0
        self.td = 0.0
        # window and logger
        self._logger = logging.getLogger('PIDTuneMethodsLog')
        self.setupUI()
        # init transfer functions
        self._proc_tf = None
        self._pid_tf = None
        self._cl_tf = None
        #init plot widgets
        self._proc_step_plot = plt.PlotWidget('Proccess Step Plot', x_axis='lin', x_label='t [sec]', y_label='mag')
        self._proc_bode_plot = plt.PlotWidget('Proccess Bode Plot', x_axis='log', x_label='w [rad/sec]', y_label='mag [dB]')
        self._cl_step_plot = plt.PlotWidget('Closed Loop Step Plot', x_axis='lin', x_label='t [sec]', y_label='mag')
        self._cl_bode_plot = plt.PlotWidget('Closed Loop Bode Plot', x_axis='log', x_label='w [rad/sec]', y_label='mag [dB]')

    def setupUI(self):
        # create window from ui
        self.ui=Ui_MainWindow()
        # setup pade-order spinbox
        self.ui.sbPadeOrder = QtGui.QSpinBox()
        self.ui.sbPadeOrder.setMinimum(0)
        self.ui.sbPadeOrder.setMaximum(10)
        self.ui.sbPadeOrder.setValue(5)
        self.ui.sbPadeOrder.setToolTip("Pade Order")
        self.ui.setupUi(self)
        # setup dialogs
        self._about_dlg = PIDTuneMethodsAboutWindow()
        # init status bar
        self._status_text = QtGui.QLabel(self.ui.centralwidget)
        self.ui.statusbar.addWidget(self._status_text, 14)
        self._refresh_status_bar(True)
        # setup toolbar
        self.ui.mainToolBar.addAction(self.ui.actionRefresh)
        self.ui.mainToolBar.addSeparator()
        self.ui.mainToolBar.addWidget(self.ui.sbPadeOrder)
        self.ui.mainToolBar.addAction(self.ui.action_P_Step_Impulse_Response)
        self.ui.mainToolBar.addAction(self.ui.action_P_Bode_Response)
        self.ui.mainToolBar.addSeparator()
        self.ui.mainToolBar.addAction(self.ui.action_CL_Step_Impulse_Response)
        self.ui.mainToolBar.addAction(self.ui.action_CL_Bode_Response)
        self.ui.mainToolBar.addSeparator()
        self.ui.mainToolBar.addAction(self.ui.actionHelp)
        self.ui.mainToolBar.addAction(self.ui.actionAbout)
        self.ui.mainToolBar.addAction(self.ui.actionExit)
        # init window objects
        self.ui.lblLambdaTauRatio.setEnabled(False)
        self.ui.leLambdaTauRatio.setEnabled(False)
        self.ui.lblLambda.setEnabled(False)
        self.ui.leLambda.setEnabled(False)
        # signals-slots
        self.ui.actionRefresh.triggered.connect(self._refresh)
        self.ui.action_P_Step_Impulse_Response.triggered.connect(self._proc_step_imp_resp)
        self.ui.action_P_Bode_Response.triggered.connect(self._proc_bode_resp)
        self.ui.action_CL_Step_Impulse_Response.triggered.connect(self._cl_step_imp_resp)
        self.ui.action_CL_Bode_Response.triggered.connect(self._cl_bode_resp)
        self.ui.actionHelp.triggered.connect(self._open_help_file)
        self.ui.actionAbout.triggered.connect(self._about_dlg.show)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.cmbProccess.currentIndexChanged.connect(self._populate_methods_list)
        self.ui.cmbTuneMethod.currentIndexChanged.connect(self._refresh_UI)
        self.ui.cmbPIDType.currentIndexChanged.connect(self._refresh_PID_fields)
        self.ui.sbPadeOrder.valueChanged.connect(self._proccess_params_changed)
        self.ui.leGain.textChanged.connect(self._proccess_params_changed)
        self.ui.leTc.textChanged.connect(self._proccess_params_changed)
        self.ui.leDeadTime.textChanged.connect(self._proccess_params_changed)
        self.ui.leLambda.textChanged.connect(self._proccess_params_changed)
        self.ui.leLambdaTauRatio.textChanged.connect(self._proccess_params_changed)
        # populate lists
        self._populate_proccess_list()
        self._populate_methods_list()
        # show window
        self.show()

    def _refresh(self):
        ''' check inputs '''
        _gain_ok = True; _tau_ok = True; _dead_time_ok = True; _lambda_ok = True
        self.gain, _gain_ok = self._check_input(self.ui.leGain.text(), "Invalid Gain")
        # First oreder with dead time
        _sel_first_order = self.ui.cmbProccess.currentText() == "First order"
        if (_sel_first_order):
            self.tau, _tau_ok = self._check_input(self.ui.leTc.text(), "Invalid Tc")
        # Lambda
        _sel_lambda = (self.ui.cmbTuneMethod.currentText() == "Lambda")
        if (_sel_lambda):
            self.dead_time, _dead_time_ok = self._check_input(self.ui.leDeadTime.text(), "Invalid Dead Time", False)
            self.lambda_tau, _lambda_ok = self._check_input(self.ui.leLambda.text(), "Invalid Lambda Value")
        else:
            self.dead_time, _dead_time_ok = self._check_input(self.ui.leDeadTime.text(), "Invalid Dead Time")
        # Integrating
        _sel_integr = (self.ui.cmbProccess.currentText() == "Integrating")
        if (_sel_integr):
            self.dead_time, _dead_time_ok = self._check_input(self.ui.leDeadTime.text(), "Invalid Dead Time", False)
        # Everything is OK ?
        _chk_ok = _gain_ok and _tau_ok and _dead_time_ok and _lambda_ok
        if (_chk_ok):
            self._set_PID_params()
            if (_sel_first_order): # first order
                # build transfer functions
                _proc_poly = ctrl.FODTPoly(self.gain, self.tau, self.dead_time, self.ui.sbPadeOrder.value())
                self._proc_tf = ctrl.TransferFunction(_proc_poly)
                self._logger.info("FODT Proc : %s" % (self._proc_tf))
                _pid_poly = ctrl.PIDPoly(self.kc, self.ti, self.td)
                self._logger.info("PID : %s" % (_pid_poly))
                _cl_poly = ctrl.closed_loop_poly(_proc_poly, _pid_poly)
                self._cl_tf = ctrl.TransferFunction(_cl_poly)
                self._refresh_status_bar(False)
            elif (_sel_integr): # integrating
                # build transfer functions
                _proc_poly = ctrl.IntgrPoly(self.gain, self.dead_time, self.ui.sbPadeOrder.value())
                self._proc_tf = ctrl.TransferFunction(_proc_poly)
                self._logger.info("Integr Proc : %s" % (self._proc_tf))
                _pid_poly = ctrl.PIDPoly(self.kc, self.ti, self.td)
                self._logger.info("PID : %s" % (_pid_poly))
                _cl_poly = ctrl.closed_loop_poly(_proc_poly, _pid_poly)
                self._cl_tf = ctrl.TransferFunction(_cl_poly)
                self._refresh_status_bar(False)
            # refresh plots
            if (self._proc_step_plot.plot_dlg.isVisible()):
                self._proc_step_imp_resp()
            if (self._proc_bode_plot.plot_dlg.isVisible()):
                self._proc_bode_resp()
            if (self._cl_step_plot.plot_dlg.isVisible()):
                self._cl_step_imp_resp()
            if (self._cl_bode_plot.plot_dlg.isVisible()):
                self._cl_bode_resp()

    def _check_input(self, val, msg, non_zero = True):
        ''' check input value'''
        try:
            _val = float(val)
        except:
            _val = 0.0
        if ((_val > 0.0 and non_zero) or
            (_val >= 0.0 and not non_zero)):
            return _val, True
        else:
            Utils.errorMessageBox(msg)
            return None, False

    def _populate_proccess_list(self):
        ''' populate methods list '''
       # populate proccess combo box
        self.ui.cmbProccess.clear()
        for i in PIDRecipe.PROCCESS:
            self.ui.cmbProccess.addItem(i)

    def _populate_methods_list(self):
        ''' populate methods list '''
       # populate methods combo box
        self.ui.cmbTuneMethod.clear()
        if (self.ui.cmbProccess.currentText() == "First order"):
            for i in PIDRecipe.PID_METHODS_FODT:
                self.ui.cmbTuneMethod.addItem(i)
                self.ui.leTc.setEnabled(True)
                self.ui.lblTc.setEnabled(True)
        elif (self.ui.cmbProccess.currentText() == "Integrating"):
            for i in PIDRecipe.PID_METHODS_I:
                self.ui.cmbTuneMethod.addItem(i)
                self.ui.leTc.setEnabled(False)
                self.ui.lblTc.setEnabled(False)

    def _refresh_UI(self, idx):
        ''' refresh UI '''
        self._populate_PID_type_list(idx)
        if (self.ui.cmbTuneMethod.currentText() == "Lambda"):
            self._refresh_lambda_fields(True)
        else:
            self._refresh_lambda_fields(False)
        self._refresh_status_bar(True)

    def _populate_PID_type_list(self, idx):
        ''' populate PID type lists '''
        # populate PID Types combo box
        self.ui.cmbPIDType.clear()
        if (self.ui.cmbProccess.currentText() == "First order"):
            for i in PIDRecipe.PID_METHODS_TYPES_FODT[idx]:
                self.ui.cmbPIDType.addItem(PIDRecipe.PID_TYPES[i])
        elif (self.ui.cmbProccess.currentText() == "Integrating"):
            for i in PIDRecipe.PID_METHODS_TYPES_I[idx]:
                self.ui.cmbPIDType.addItem(PIDRecipe.PID_TYPES[i])

    def _refresh_lambda_fields(self, en):
        ''' enable-disable lambda fields '''
        self.ui.lblLambda.setEnabled(en)
        self.ui.leLambda.setEnabled(en)
        self.ui.lblLambdaTauRatio.setEnabled(en)
        self.ui.leLambdaTauRatio.setEnabled(en)

    def _refresh_PID_fields(self, idx):
        ''' refresh PID fields '''
        if (self.ui.cmbPIDType.currentText() == "P"):
            self.ui.lblKc.setEnabled(True)
            self.ui.lblTi.setEnabled(False)
            self.ui.lblTd.setEnabled(False)
            self.ui.leKc.setEnabled(True)
            self.ui.leTi.setEnabled(False)
            self.ui.leTd.setEnabled(False)
        elif (self.ui.cmbPIDType.currentText() == "PI"):
            self.ui.lblKc.setEnabled(True)
            self.ui.lblTi.setEnabled(True)
            self.ui.lblTd.setEnabled(False)
            self.ui.leKc.setEnabled(True)
            self.ui.leTi.setEnabled(True)
            self.ui.leTd.setEnabled(False)
        elif (self.ui.cmbPIDType.currentText() == "PID"):
            self.ui.lblKc.setEnabled(True)
            self.ui.lblTi.setEnabled(True)
            self.ui.lblTd.setEnabled(True)
            self.ui.leKc.setEnabled(True)
            self.ui.leTi.setEnabled(True)
            self.ui.leTd.setEnabled(True)
        self._refresh_status_bar(True)

    def _proccess_params_changed(self):
        ''' proccess params changed '''
        self._refresh_status_bar(True)

    def _refresh_status_bar(self, needs_refresh):
        """update status bar"""
        if (needs_refresh):
            msg = "    Status : %s" % 'Refresh is needed...'
            self.ui.statusbar.setStyleSheet('QLabel {background-color : gray; color : yellow;}')
        else:
            msg = "    Status : %s" % 'OK'
            self.ui.statusbar.setStyleSheet('QLabel {background-color : green; color : white;}')
        self._status_text.setText(msg)

    def _set_PID_params(self):
        ''' set PID params for predefined PIDs '''
        self._logger.info("Gain : %.2f, Tc : %.2f, Dead Time : %.2f,Lambda value : %.2f" % (self.gain, self.tau, self.dead_time, self.lambda_tau))
        if (self.ui.cmbProccess.currentText() == "First order"):
            _method = PIDRecipe.PID_METHODS_TYPES_FODT[self.ui.cmbTuneMethod.currentIndex()]
            _method_str = self.ui.cmbTuneMethod.currentText()
            _type = _method[self.ui.cmbPIDType.currentIndex()]
            if (_method_str == "Lambda"):
                _kc, _ti, _td = PIDRecipe.PID_RECIPIES_FODT[self.ui.cmbTuneMethod.currentIndex()](_type, self.gain, self.tau, self.dead_time, self.lambda_tau)
                self.ui.leLambdaTauRatio.setText('{:.4}'.format(self.lambda_tau / self.tau))
            else:
                _kc, _ti, _td = PIDRecipe.PID_RECIPIES_FODT[self.ui.cmbTuneMethod.currentIndex()](_type, self.gain, self.tau, self.dead_time)
        elif (self.ui.cmbProccess.currentText() == "Integrating"):
            _method = PIDRecipe.PID_METHODS_TYPES_I[self.ui.cmbTuneMethod.currentIndex()]
            _method_str = self.ui.cmbTuneMethod.currentText()
            _type = _method[self.ui.cmbPIDType.currentIndex()]
            if (_method_str == "Lambda"):
                self.ui.leLambdaTauRatio.setText('0.0')
                _kc, _ti, _td = PIDRecipe.PID_RECIPIES_I[self.ui.cmbTuneMethod.currentIndex()](_type, self.gain, None, self.dead_time, self.lambda_tau)
        self.ui.leKc.setText('{:.4}'.format(_kc))
        self.ui.leTi.setText('{:.4}'.format(_ti))
        self.ui.leTd.setText('{:.4}'.format(_td))
        self.kc = _kc
        self.ti = _ti
        self.td = _td

    def _proc_step_imp_resp(self):
        '''proccess step - impulse response'''
        if (self._proc_tf):
            self._proc_step_plot.del_curves()
            t, y = self._proc_tf.step()
            self._proc_step_plot.add_curve(t, y, 'Step', 'b')
            #t, y = self._proc_tf.impulse()
            #self._proc_step_plot.add_curve(t, y, 'Impulse', 'r')
            self._proc_step_plot.show()
            self._logger.info("Proccess Time Graphs opened.")
        else:
            self._logger.warning("Proccess Time Graphs failed > Invalid Proccess Model.")
            Utils.errorMessageBox("Invalid Proccess Model")

    def _proc_bode_resp(self):
        '''proccess bode response'''
        if (self._proc_tf):
            self._proc_bode_plot.del_curves()
            w, mag, phase = self._proc_tf.bode()
            self._proc_bode_plot.add_curve(w, mag, 'Mag', 'b')
            #self._proc_bode_plot.add_curve(w, phase, 'Phase', 'r')
            self._proc_bode_plot.show()
            self._logger.info("Proccess Bode Graphs opened.")
        else:
            self._logger.warning("Proccess Bode Graphs failed > Invalid Proccess Model.")
            Utils.errorMessageBox("Invalid Proccess Model")

    def _cl_step_imp_resp(self):
        '''closed loop step - impulse response'''
        if (self._cl_tf):
            self._cl_step_plot.del_curves()
            t, y = self._cl_tf.step()
            self._cl_step_plot.add_curve(t, y, 'Step', 'b')
            #t, y = self._cl_tf.impulse()
            #self._cl_step_plot.add_curve(t, y, 'Impulse', 'r')
            self._cl_step_plot.show()
            self._logger.info("Closed Loop Time Graphs opened.")
        else:
            self._logger.warning("Closed Loop Time Graphs failed > Invalid Closed Loop Model.")
            Utils.errorMessageBox("Invalid Closed Loop Model")

    def _cl_bode_resp(self):
        '''closed loop bode response'''
        if (self._cl_tf):
            self._cl_bode_plot.del_curves()
            w, mag, phase = self._cl_tf.bode()
            self._cl_bode_plot.add_curve(w, mag, 'Mag', 'b')
            #self._cl_bode_plot.add_curve(w, phase, 'Phase', 'r')
            self._cl_bode_plot.show()
            self._logger.info("Closed Loop Bode Graphs opened.")
        else:
            self._logger.warning("Closed Loop Bode Graphs failed > Invalid Closed Loop Model.")
            Utils.errorMessageBox("Invalid Closed Loop Model")

    def _open_help_file(self):
        '''open help file'''
        _path = os.path.dirname(sys.argv[0])
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file:///" + _path + "/PIDTuneMethods.html"))

    def closeEvent(self,QCloseEvent):
        """window is closing"""
        self._proc_step_plot.plot_dlg.close()
        self._proc_bode_plot.plot_dlg.close()
        self._cl_step_plot.plot_dlg.close()
        self._cl_bode_plot.plot_dlg.close()

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def main():

    #create logger
    logger = Utils.create_logger(logger_name='PIDTuneMethodsLog', level=logging.DEBUG)
    Utils.set_up_logger_file(logger, 'pyPIDTuneMethods.log')
    #create qt application
    app=QtGui.QApplication(sys.argv)
    #load main window
    w = PIDTuneMethodsWindow()
    #application loop
    res = sys.exit(app.exec_())
    #application loop quited

if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------