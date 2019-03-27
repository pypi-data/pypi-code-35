# -*- coding: utf-8 -*-
"""
A python package for audio I/O based on `spAudio
<http://www-ie.meijo-u.ac.jp/labs/rj001/spLibs/index.html>`_.

Example:
    The following is the example to realize fullduplex audio I/O.
    ::

        import spaudio

        a = spaudio.SpAudio()

        a.setnchannels(2)
        a.setsamprate(44100)
        a.setbuffersize(2048)

        nloop = 500
        b = bytearray(4096)

        a.open('r')
        a.open('w')

        for i in range(nloop):
            a.readraw(b)
            a.writeraw(b)

        a.close()
"""

import locale
import math
import array
from _spaudio import spaudio_c as _spaudio_c


__version__ = '0.7.13'

OUTPUT_POSITION_CALLBACK = (1 << 0)
OUTPUT_BUFFER_CALLBACK = (1 << 2)

_audio_global = None
_encoding = locale.getpreferredencoding()
_defaultdrivername = _spaudio_c.xspGetAudioDriverName(0)
if isinstance(_defaultdrivername, bytes):
    _ischarbinary = True
else:
    _ischarbinary = False


class Error(Exception):
    """Base exception class for spaudio."""
    pass


class DriverError(Error):
    """Exception raised by audio driver problems."""
    pass


class DeviceError(Error):
    """Exception raised by audio device problems."""
    pass


def callbacksignature(audio, calltype, cbdata, args):
    """Signature of the callback function for :func:`~spaudio.SpAudio.setcallback` method.

    Args:
        audio (SpAudio): An instance of SpAudio class.
        calltype (int): The callback type.
            OUTPUT_POSITION_CALLBACK or OUTPUT_BUFFER_CALLBACK.
        cbdata: callback-depend data.
            a position (int) on OUTPUT_POSITION_CALLBACK
            or a buffer (bytes) on OUTPUT_BUFFER_CALLBACK.
        args: Variable length argument list specified at :func:`~spaudio.SpAudio.setcallback`.
            Note that this 'args' variable does not require the prefix '*'.

    Returns:
        bool: False if you don't want to fire callbacks anymore.
    """
    return True


class SpAudio:
    """A class for audio I/O.

    Args:
        driver_name (str): the driver name to initialize.
    """
    def __init__(self, drivername=None):
        self._audio = None
        self._read_mode = ' '
        self._write_mode = ' '
        self._initdriver(drivername)

    def __del__(self):
        self.terminate()

    def reload(self, drivername=None):
        """Reloads a new audio driver."""
        self.terminate()
        self._initdriver(drivername)

    def terminate(self):
        """Terminates the current audio driver."""
        if self._audio is not None:
            _spaudio_c._spFreeAudioDriver(self._audio)
            global _audio_global
            _audio_global = None
            self._audio = None

    def _initdriver(self, drivername=None):
        """Initializes the audio driver."""
        if drivername is not None:
            global _ischarbinary
            if _ischarbinary:
                global _encoding
                encodedname = drivername.encode(_encoding)
            else:
                encodedname = drivername
        else:
            encodedname = None
        global _audio_global
        if _audio_global is not None:
            self._audio = _audio_global
        else:
            self._audio = _spaudio_c.spInitAudioDriver(encodedname)
            if self._audio is None:
                raise DriverError('cannot load audio driver')
            _audio_global = self._audio

    def getndevices(self):
        """Gets the number of audio devices."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, numdevice = _spaudio_c.spGetNumAudioDevice(self._audio)
        if flag:
            return numdevice
        else:
            raise DriverError('audio driver error')

    def getdevicename(self, deviceindex):
        """Gets the name of the audio device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if deviceindex < 0 or deviceindex >= self.getndevices():
            raise ValueError('0 <= index < %d is required'
                             % self.getndevices())
        name = _spaudio_c.xspGetAudioDeviceName(self._audio, deviceindex)
        if name is not None:
            global _ischarbinary
            if _ischarbinary:
                global _encoding
                return name.decode(_encoding)
            else:
                return name
        else:
            raise DriverError('audio driver error')

    def getdevicelist(self):
        """Gets the list of audio devices."""
        list = []
        for i in range(self.getndevices()):
            list.append(self.getdevicename(i))
        return list

    def selectdevice(self, deviceindex):
        """Selects an audio device which has the index specified."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if deviceindex < 0 or deviceindex >= self.getndevices():
            raise ValueError('0 <= index < %d is required'
                             % self.getndevices())
        flag = _spaudio_c.spSelectAudioDevice(self._audio, deviceindex)
        if not flag:
            raise DriverError('cannot select the audio device')

    def setcallback(self, calltype, func, *args):
        """Sets a callback function.

        Args:
            calltype (int): A combination of callback types.
                OUTPUT_POSITION_CALLBACK and OUTPUT_BUFFER_CALLBACK
                are supported currently.
            func (callable): Callback function. The callback must have
                a signature in the :func:`~spaudio.callbacksignature` document.
            *args: Variable length argument list.
        """
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spSetAudioCallbackFunc_(self._audio, calltype, (func, self, args))
        if not flag:
            raise DriverError('cannot set a callback function')

    def setsamprate(self, samprate):
        """Sets sample rate of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spSetAudioSampleRate(self._audio, samprate)
        if not flag:
            raise DriverError('audio driver error')

    def getsamprate(self):
        """Gets sample rate of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, samprate = _spaudio_c.spGetAudioSampleRate(self._audio)
        if flag:
            return samprate
        else:
            raise DriverError('audio driver error')

    def setsampbit(self, sampbit):
        """Sets bits/sample of the current device. sampbit = 33 means
        32bit float."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if sampbit < 8:
            raise ValueError('sampbit >= 8 is required')
        flag = _spaudio_c.spSetAudioSampleBit(self._audio, sampbit)
        if not flag:
            raise DriverError('audio driver error')

    def setsampwidth(self, sampwidth, floatflag=False):
        """Sets bytes/sample of the current device."""
        sampbit = sampwidth * 8
        if floatflag:
            sampbit += 1
        return self.setsampbit(sampbit)

    def getsampbit(self):
        """Gets bits/sample of the current device. sampbit = 33 means
        32bit float."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, sampbit = _spaudio_c.spGetAudioSampleBit(self._audio)
        if flag:
            return sampbit
        else:
            raise DriverError('audio driver error')

    def getsampwidth(self):
        """Gets bytes/sample of the current device."""
        return math.floor(self.getsampbit() / 8)

    def getrawsampbit(self):
        """Gets the bits/sample specified."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, sampbit = _spaudio_c.spGetAudioSpecifiedSampleBit(self._audio)
        if flag:
            return sampbit
        else:
            raise DriverError('audio driver error')

    def getrawsampwidth(self):
        """Gets the bytes/sample specified."""
        return math.floor(self.getrawsampbit() / 8)

    def setnchannels(self, nchannels):
        """Sets the number of channels of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if nchannels <= 0:
            raise ValueError('nchannels >= 1 is required')
        flag = _spaudio_c.spSetAudioChannel(self._audio, nchannels)
        if not flag:
            raise DriverError('audio driver error')

    def getnchannels(self):
        """Gets the number of channels of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, nchannels = _spaudio_c.spGetAudioChannel(self._audio)
        if flag:
            return nchannels
        else:
            raise DriverError('audio driver error')

    def setbuffersize(self, buffersize):
        """Sets the buffer size of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spSetAudioBufferSize(self._audio, buffersize)
        if not flag:
            raise DriverError('audio driver error')

    def getbuffersize(self):
        """Gets the buffer size of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, buffersize = _spaudio_c.spGetAudioBufferSize(self._audio)
        if flag:
            return buffersize
        else:
            raise DriverError('audio driver error')

    def setnbuffers(self, nbuffers):
        """Sets the number of buffers of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if nbuffers <= 0:
            raise ValueError('nbuffers >= 1 is required')
        flag = _spaudio_c.spSetAudioNumBuffer(self._audio, nbuffers)
        if not flag:
            raise DriverError('audio driver error')

    def getnbuffers(self):
        """Gets the number of buffers of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, nbuffers = _spaudio_c.spGetAudioNumBuffer(self._audio)
        if flag:
            return nbuffers
        else:
            raise DriverError('audio driver error')

    def setblockingmode(self, mode):
        """Sets the blocking mode of the current device.

        Args:
            mode (int): 0 = blocking mode (default), 1 = nonblocking mode."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spSetAudioBlockingMode(self._audio, mode)
        if not flag:
            raise DriverError('audio driver error')

    def getblockingmode(self):
        """Gets the blocking mode of the current device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag, mode = _spaudio_c.spGetAudioBlockingMode(self._audio)
        if flag:
            return mode
        else:
            raise DriverError('audio driver error')

    def open(self, mode):
        """Opens the current audio device.

        Args:
            mode (str): Device opening mode. 'r' means read mode, 'w' means
                        write mode. 'ro' and 'wo' which mean read only and
                        write only modes are also supported. Although these modes
                        validate only the specified mode, some environments recieve
                        a benefit that the processing becomes faster.
        """
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if mode[0] == 'r':
            if self._write_mode[-1] == 'o':
                raise RuntimeError('device has been opened with write only mode')
            elif self._read_mode[0] == 'r':
                raise RuntimeError('device has already been opened')
            self._read_mode = mode
        elif mode[0] == 'w':
            if self._read_mode[-1] == 'o':
                raise RuntimeError('device has been opened with read only mode')
            elif self._write_mode[0] == 'w':
                raise RuntimeError('device has already been opened')
            self._write_mode = mode
        else:
            raise RuntimeError('unknown open mode: %s' % mode)
        global _ischarbinary
        if _ischarbinary:
            mode2 = mode.encode('utf-8')
        else:
            mode2 = mode
        flag = _spaudio_c.spOpenAudioDevice(self._audio, mode2)
        if not flag:
            raise DeviceError('cannot open audio device')

    def close(self):
        """Closes the current audio device."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spCloseAudioDevice(self._audio)
        self._read_mode = ' '
        self._write_mode = ' '
        if not flag:
            raise DeviceError('cannot close audio device')

    def stop(self):
        """Stops audio I/O."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spStopAudio(self._audio)
        if not flag:
            raise DeviceError('cannot stop audio I/O')

    def sync(self):
        """Synchronizes audio I/O."""
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        flag = _spaudio_c.spSyncAudio(self._audio)
        if not flag:
            raise DeviceError('cannot synchronize audio I/O')

    def getrawarraytypecode(self):
        """Gets the type code for python array.

        Returns:
            char: A type code for the current settings.
        """
        sampbit = self.getrawsampbit()
        if sampbit >= 64:
            typecode = 'd'
        elif sampbit >= 33:
            typecode = 'f'
        elif sampbit >= 32:
            typecode = 'l'
        else:
            typecode = 'h'
        return typecode

    def createrawarray(self, length):
        """Creates a raw array for the current device settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).

        Returns:
            array.array: An array class object for the current device settings.
        """
        size = length * self.getrawsampwidth()
        buffer = bytearray(size)
        return array.array(self.getrawarraytypecode(), buffer)

    def getarraytypecode(self):
        """Gets the type code for python array to store double array.

        Returns:
            char: A type code of double array for the current settings.
        """
        return 'd'

    def createarray(self, length):
        """Creates a double array for the current device settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).

        Returns:
            array.array: An array class object for the current device settings.
        """
        size = length * 8
        buffer = bytearray(size)
        return array.array(self.getarraytypecode(), buffer)

    def getrawndarraydtype(self):
        """Gets the dtype string for numpy ndarray.

        Returns:
            string: a dtype string for the current settings.
        """
        sampbit = self.getrawsampbit()
        if sampbit >= 64:
            dtypestr = 'f8'
        elif sampbit >= 33:
            dtypestr = 'f4'
        elif sampbit >= 32:
            dtypestr = 'i4'
        else:
            dtypestr = 'i2'
        return dtypestr

    def createrawndarray(self, length):
        """Creates a raw numpy ndarray for the current device settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).

        Returns:
            numpy.ndarray: An ndarray class object for the current device settings.
        """
        import numpy as np
        size = length * self.getrawsampwidth()
        buffer = bytearray(size)
        return np.frombuffer(buffer, dtype=self.getrawndarraydtype())

    def getndarraydtype(self):
        """Gets the dtype string for numpy ndarray to store double array.

        Returns:
            string: a dtype string for the current settings.
        """
        return 'f8'

    def createndarray(self, length):
        """Creates a numpy double array for the current device settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).

        Returns:
            numpy.ndarray: An ndarray class object for the current device settings.
        """
        import numpy as np
        size = length * 8
        buffer = bytearray(size)
        return np.frombuffer(buffer, dtype=self.getndarraydtype())

    def readraw(self, data):
        """Reads raw data from the audio device.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer to receive raw data from the audio device.

        Returns:
            int: The read size if successful, -1 otherwise.
        """
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._read_mode[0] != 'r':
            raise RuntimeError('device must be opened with read mode')
        if isinstance(data, bytearray):
            buffer = data
        elif isinstance(data, array.array):
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')
        nread = _spaudio_c.spReadAudioBuffer(self._audio, buffer)
        return nread / self.getrawsampwidth() if nread > 0 else nread

    def writeraw(self, data):
        """Writes raw data to the audio device.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer to send raw data to the audio device.

        Returns:
            int: The written size if successful, -1 otherwise.
        """
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._write_mode[0] != 'w':
            raise RuntimeError('device must be opened with write mode')
        if isinstance(data, bytearray) or isinstance(data, bytes):
            buffer = data
        elif isinstance(data, array.array):
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')
        nwrite = _spaudio_c.spWriteAudioBuffer(self._audio, buffer)
        return nwrite / self.getrawsampwidth() if nwrite > 0 else nwrite

    def read(self, data, weight=1.0):
        """Reads data to double array from the audio device.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer of double array to receive data from the audio device.
            weight (double): a weighting factor multiplied to data after reading.

        Returns:
            int: The read size if successful, -1 otherwise.
        """
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._read_mode[0] != 'r':
            raise RuntimeError('device must be opened with read mode')
        if isinstance(data, bytearray):
            buffer = data
        elif isinstance(data, array.array):
            if data.typecode != 'd':
                raise RuntimeError('the typecode must be \'d\'')
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            if not np.issubdtype('f8', data.dtype):
                raise RuntimeError('the dtype must be \'f8\' (\'float64\')')
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')
        return _spaudio_c.spReadAudioDoubleBufferWeighted_(self._audio, buffer, weight)

    def write(self, data, weight=1.0):
        """Writes data of double array to the audio device.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer of double array to send data to the audio device.
            weight (double): A weighting factor multiplied to data before writing.

        Returns:
            int: The written size if successful, -1 otherwise.
        """
        if self._audio is None:
            raise RuntimeError('driver must be loaded')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._write_mode[0] != 'w':
            raise RuntimeError('device must be opened with write mode')
        if isinstance(data, bytearray) or isinstance(data, bytes):
            buffer = data
        elif isinstance(data, array.array):
            if data.typecode != 'd':
                raise RuntimeError('the typecode must be \'d\'')
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            if not np.issubdtype('f8', data.dtype):
                raise RuntimeError('the dtype must be \'f8\' (\'float64\')')
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')
        return _spaudio_c.spWriteAudioDoubleBufferWeighted_(self._audio, buffer, weight)


def getndrivers():
    """Gets the number of drivers."""
    return _spaudio_c.spGetNumAudioDriver()


def getdrivername(index):
    """Gets the name of the driver which has the index specified."""
    if index < 0 or index >= getndrivers():
        raise ValueError('0 <= index < %d is required'
                         % getndrivers())
    name = _spaudio_c.xspGetAudioDriverName(index)
    if name is not None:
        global _ischarbinary
        if _ischarbinary:
            return name.decode(locale.getpreferredencoding())
        else:
            return name
    else:
        raise DriverError('audio driver error')


def getdriverlist():
    """Gets a list of driver names."""
    list = []
    for i in range(getndrivers()):
        list.append(getdrivername(i))
    return list


def getndriverdevices(drivername=None):
    """Gets the number of devices in the driver."""
    if drivername is not None:
        global _ischarbinary
        if _ischarbinary:
            encodedname = drivername.encode(locale.getpreferredencoding())
        else:
            encodedname = drivername
    else:
        encodedname = None
    return _spaudio_c.spGetNumAudioDriverDevice(encodedname)


def getdriverdevicename(index, drivername=None):
    """Gets the name of the device in the driver."""
    global _ischarbinary
    if index < 0 or index >= getndriverdevices(drivername):
        raise ValueError('0 <= index < %d is required'
                         % getndriverdevices(drivername))
    if drivername is not None:
        if _ischarbinary:
            encodedname = drivername.encode(locale.getpreferredencoding())
        else:
            encodedname = drivername
    else:
        encodedname = None
    devicename = _spaudio_c.xspGetAudioDriverDeviceName(encodedname, index)
    if devicename is not None:
        if _ischarbinary:
            return devicename.decode(locale.getpreferredencoding())
        else:
            return devicename
    else:
        return ''


if __name__ == '__main__':
    driverlist = getdriverlist()
    for i in range(getndrivers()):
        print('Driver %d: %s' % (i, driverlist[i]))
        for j in range(getndriverdevices(driverlist[i])):
            print('    Device %d: %s'
                  % (j, getdriverdevicename(j, driverlist[i])))
