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
  rx_sample_rates = (48000, 96000, 192000, 240000, 288000, 384000, 480000, 768000, 960000,
                   1152000, 1536000, 1920000, 2304000)
  def __init__(self, app, conf):
    BaseHardware.__init__(self, app, conf)
    self.vardecim_index = 1
    self.fVFO = 0.0	# Careful, this is a float
  def open(self):	# Called once to open the Hardware
    if not soapy:
      return "Soapy module not available"
    radio_dict = self.application.local_conf.GetRadioDict()
    device = radio_dict.get('soapy_device', '')
    txt = soapy.open_device(device, 1, self.conf.data_poll_usec)
    rate = self.rx_sample_rates[self.vardecim_index]
    soapy.set_parameter('soapy_setSampleRate_rx', '', float(rate))
    soapy.set_parameter('soapy_setAntenna_rx', radio_dict['soapy_setAntenna_rx'], 0.0)
    self.ChangeRxGain()
    return txt
  def ChangeRxGain(self):
    if not soapy:
      return
    radio_dict = self.application.local_conf.GetRadioDict()
    gain_mode = radio_dict['soapy_gain_mode_rx']
    gain_values = radio_dict['soapy_gain_values_rx']
    if gain_mode == 'automatic':
      soapy.set_parameter('soapy_setGainMode_rx', 'true', 0.0)
    elif gain_mode == 'total':
      soapy.set_parameter('soapy_setGainMode_rx', 'false', 0.0)
      gain = gain_values.get('total', '0')
      gain = float(gain)
      soapy.set_parameter('soapy_setGain_rx', '', gain)
    elif gain_mode == 'detailed':
      soapy.set_parameter('soapy_setGainMode_rx', 'false', 0.0)
      for name, dmin, dmax, dstep in radio_dict.get('soapy_listGainsValues_rx', ()):
        if name == 'total':
          continue
        gain = gain_values.get(name, '0')
        gain = float(gain)
        soapy.set_parameter('soapy_setGainElement_rx', name, gain)
  def close(self):			# Called once to close the Hardware
    if soapy:
      soapy.close_device(1)
  def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
    fVFO = float(vfo)
    if self.fVFO != fVFO:
      self.fVFO = fVFO
      if soapy:
        soapy.set_parameter('soapy_setFrequency_rx', '', fVFO)
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
  def ChangeMode(self, mode):		# Change the tx/rx mode
    # mode is a string: "USB", "AM", etc.
    pass
  def ChangeBand(self, band):
    # band is a string: "60", "40", "WWV", etc.
    try:
      self.transverter_offset = self.conf.bandTransverterOffset[band]
    except:
      self.transverter_offset = 0
  def OnBtnFDX(self, is_fdx):   # Status of FDX button, 0 or 1
    pass
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
        self.vardecim_index = 2
    else:
      self.vardecim_index = index
    rate = self.rx_sample_rates[self.vardecim_index]
    if soapy:
      soapy.set_parameter('soapy_setSampleRate_rx', '', float(rate))
      soapy.set_parameter('soapy_setFrequency_rx', '', self.fVFO)	# driver Lime requires reset of Rx freq on sample rate change
    return rate
  def VarDecimRange(self):  # Return the lowest and highest sample rate.
    return self.rx_sample_rates[0], self.rx_sample_rates[-1]
