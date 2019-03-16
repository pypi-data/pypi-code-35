"""
PulseWaveform.py
"""

# Copyright (c) 2018 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

from SignalIntegrity.Lib.TimeDomain.Waveform.Waveform import Waveform
from SignalIntegrity.Lib.TimeDomain.Waveform.StepWaveform import StepWaveform

class PulseWaveform(Waveform):
    """pulse waveform"""
    def __init__(self,td,Amplitude=1.,StartTime=0.,PulseWidth=0):
        """Constructor

        constructs a waveform with mean and normally distributed noise.

        @param td instance of class TimeDescriptor containing time axis of waveform.
        @param Amplitude (optional) float amplitude of pulse (defaults to unity).
        @param StartTime (optional) float starting time of the pulse (defaults to zero).
        @param PulseWidth (optional) float the width of the pulse (defaults to zero).

        @note The amplitude can be positive or negative, with negative providing a negative
        pulse.
        @note if the pulse appears entirely within the samples, then the waveform will be all zero.
        """
        StopTime=StartTime+PulseWidth
        stepup=StepWaveform(td,Amplitude,StartTime)
        stepdown=StepWaveform(td,Amplitude,StopTime)
        Waveform.__init__(self,td,[stepup[k]-stepdown[k] for k in range(len(stepup))])