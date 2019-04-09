# This is the hardware file to support radios accessed by the SoapySDR interface.

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import socket, traceback, time, math
import _quisk as QS
try:
  from soapypkg import soapy
except:
  #traceback.print_exc()
  soapy = None

from quisk_hardware_model import Hardware as BaseHardware

DEBUG = 0

class Hardware(BaseHardware):
  def __init__(self, app, conf):
    BaseHardware.__init__(self, app, conf)
    self.vardecim_index = 0
    self.fVFO = 0.0	# Careful, this is a float
    radio_dict = self.application.local_conf.GetRadioDict()
    self.rx_sample_rates = radio_dict.get('soapy_sample_rates_rx', [48000])
  def pre_open(self):
    pass
  def open(self):	# Called once to open the Hardware
    if not soapy:
      return "Soapy module not available"
    radio_dict = self.application.local_conf.GetRadioDict()
    device = radio_dict.get('soapy_device', '')
    txt = soapy.open_device(device, 1, self.conf.data_poll_usec)
    rate = self.rx_sample_rates[self.vardecim_index]
    soapy.set_parameter('soapy_setSampleRate_rx', '', float(rate))
    rate = radio_dict.get('soapy_sample_rate_tx', 48000)
    QS.set_tx_audio(tx_sample_rate=rate)
    soapy.set_parameter('soapy_setSampleRate_tx', '', float(rate))
    soapy.set_parameter('soapy_setAntenna_rx', radio_dict['soapy_setAntenna_rx'], 0.0)
    soapy.set_parameter('soapy_setAntenna_tx', radio_dict['soapy_setAntenna_tx'], 0.0)
    self.ChangeGain('_rx')
    self.ChangeGain('_tx')
    return txt
  def ChangeGain(self, rxtx):	# rxtx is '_rx' or '_tx'
    if not soapy:
      return
    radio_dict = self.application.local_conf.GetRadioDict()
    gain_mode = radio_dict['soapy_gain_mode' + rxtx]
    gain_values = radio_dict['soapy_gain_values' + rxtx]
    if gain_mode == 'automatic':
      soapy.set_parameter('soapy_setGainMode' + rxtx, 'true', 0.0)
    elif gain_mode == 'total':
      soapy.set_parameter('soapy_setGainMode' + rxtx, 'false', 0.0)
      gain = gain_values.get('total', '0')
      gain = float(gain)
      soapy.set_parameter('soapy_setGain' + rxtx, '', gain)
    elif gain_mode == 'detailed':
      soapy.set_parameter('soapy_setGainMode' + rxtx, 'false', 0.0)
      for name, dmin, dmax, dstep in radio_dict.get('soapy_listGainsValues' + rxtx, ()):
        if name == 'total':
          continue
        gain = gain_values.get(name, '0')
        gain = float(gain)
        soapy.set_parameter('soapy_setGainElement' + rxtx, name, gain)
  def close(self):			# Called once to close the Hardware
    if soapy:
      soapy.close_device(1)
  def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
    fVFO = float(vfo)
    if self.fVFO != fVFO:
      self.fVFO = fVFO
      if soapy:
        soapy.set_parameter('soapy_setFrequency_rx', '', fVFO)
    #if soapy:
    #  soapy.set_parameter('soapy_setFrequency_tx', '', float(tune))
    return tune, vfo
  def ReturnFrequency(self):
    # Return the current tuning and VFO frequency.  If neither have changed,
    # you can return (None, None).  This is called at about 10 Hz by the main.
    # return (tune, vfo)	# return changed frequencies
    return None, None		# frequencies have not changed
  def ReturnVfoFloat(self):
    # Return the accurate VFO frequency as a floating point number.
    # You can return None to indicate that the integer VFO frequency is valid.
    return None
  def OnBtnFDX(self, fdx):	# fdx is 0 or 1
    if soapy:
      soapy.set_parameter('soapy_FDX', '', float(fdx))
  def OnButtonPTT(self, event):
    btn = event.GetEventObject()
    if btn.GetValue():
      QS.set_PTT(1)
      QS.set_key_down(1)
    else:
      QS.set_PTT(0)
      QS.set_key_down(0)
  def OnSpot(self, level):
    # level is -1 for Spot button Off; else the Spot level 0 to 1000.
    pass
  def ChangeMode(self, mode):		# Change the tx/rx mode
    # mode is a string: "USB", "AM", etc.
    pass
  def ChangeBand(self, band):
    # band is a string: "60", "40", "WWV", etc.
    try:
      self.transverter_offset = self.conf.bandTransverterOffset[band]
    except:
      self.transverter_offset = 0
  def HeartBeat(self):	# Called at about 10 Hz by the main
    pass
  # The "VarDecim" methods are used to change the hardware decimation rate.
  # If VarDecimGetChoices() returns any False value, no other methods are called.
  def VarDecimGetChoices(self):	# Return a list/tuple of strings for the decimation control.
    return map(str, self.rx_sample_rates)
  def VarDecimGetLabel(self):	# Return a text label for the decimation control.
    return 'Receiver Sample Rate'
  def VarDecimGetIndex(self):	# Return the index 0, 1, ... of the current decimation.
    return self.vardecim_index		# This is called before open() to initialize the control.
  def VarDecimSet(self, index=None):	# Called when the control is operated; if index==None, called on startup.
    if index is None:
      try:		# vardecim_set is the sample rate
        self.vardecim_index = self.rx_sample_rates.index(int(self.application.vardecim_set))
      except:
        self.vardecim_index = 0
    else:
      self.vardecim_index = index
    rate = self.rx_sample_rates[self.vardecim_index]
    if soapy:
      soapy.set_parameter('soapy_setSampleRate_rx', '', float(rate))
      soapy.set_parameter('soapy_setFrequency_rx', '', self.fVFO)	# driver Lime requires reset of Rx freq on sample rate change
    return rate
  def VarDecimRange(self):  # Return the lowest and highest sample rate.
    return self.rx_sample_rates[0], self.rx_sample_rates[-1]
