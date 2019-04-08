## binhoHostAdapter Python Library
##
## Jonathan Georgino <jonathan@binho.io>
## Binho Electronics
## www.binho.io

import threading
import queue
import signal
import sys
import serial
from time import sleep

class SerialPortManager(threading.Thread):

        serialPort = None
        txdQueue = None
        rxdQueue = None
        intQueue = None
        stopper = None

        def __init__(self, serialPort, txdQueue, rxdQueue, intQueue, stopper):
            super().__init__()
            self.serialPort = serialPort
            self.txdQueue = txdQueue
            self.rxdQueue = rxdQueue
            self.intQueue = intQueue
            self.stopper = stopper

        def run(self):

            comport = serial.Serial(self.serialPort, baudrate=1000000, timeout=0.025)

            while not self.stopper.is_set():

                if comport.in_waiting > 0:
                    receivedData = comport.readline().strip().decode("utf-8")

                    if receivedData[0] == '!':
                        self.intQueue.put(receivedData)
                    else:
                        self.rxdQueue.put(receivedData)

                if self.txdQueue.empty() == False:
                    serialCommand = self.txdQueue.get() + '\n'
                    comport.write(serialCommand.encode("utf-8"))

class SignalHandler:
    """
    The object that will handle signals and stop the worker threads.
    """

    #: The stop event that's shared by this handler and threads.
    stopper = None

    #: The pool of worker threads
    workers = None

    def __init__(self, stopper, manager):
        self.stopper = stopper
        self.manager = manager

    def __call__(self, signum, frame):
        """
        This will be called by the python signal module
        https://docs.python.org/3/library/signal.html#signal.signal
        """
        self.stopper.set()

        self.manager.join()

        sys.exit(0)

class binhoHostAdapter:

    # Constructor, needs a serial port as a parameter

    def __init__(self, serialPort):

        self.serialPort = serialPort

        self.interrupts = set()

        self._stopper = threading.Event()
        self._txdQueue = queue.Queue()
        self._rxdQueue = queue.Queue()
        self._intQueue = queue.Queue()

        # we need to keep track of the workers but not start them yet
        #workers = [StatusChecker(url_queue, result_queue, stopper) for i in range(num_workers)]
        self.manager = SerialPortManager(self.serialPort, self._txdQueue, self._rxdQueue, self._intQueue, self._stopper)

        # create our signal handler and connect it
        self.handler = SignalHandler(self._stopper, self.manager)
        signal.signal(signal.SIGINT, self.handler)

        # start the threads!
        self.manager.daemon = True

        self.manager.start()

    # Private functions

    def _sendCommand(self, command):

        self._txdQueue.put(command)

    def _readResponse(self):

        result = self._rxdQueue.get()

        return result

    def _checkInterrupts(self):

        while self._intQueue.empty() == False:
            self.interrupts.add(self._intQueue.get())

    # Public functions

    # Communication Management

    def open(self):

        self.interrupts.clear()
        self.manager.start()

    def close(self):

        self._stopper.set()

    def interruptCount(self):

        self._checkInterrupts()

        return len(self.interrupts)

    def interruptCheck(self, interrupt):

        self._checkInterrupts()

        if interrupt in self.interrupts:
            return True
        else:
            return False

    def interruptClear(self, interrupt):

        self.interrupts.discard(interrupt)

    def interruptClearAll(self):

        self.interrupts.clear()

    def getInterrupts(self):

        self._checkInterrupts()

        return self.interrupts.copy()

    ## DEVICE COMMANDS

    def echo(self):

        self._sendCommand('+ECHO')
        result = self._readResponse()

        return result

    def ping(self):

        self._sendCommand('+PING')
        result = self._readResponse()

        return result

    ## GET/SET OperationMode
    ##
    ## parameters:
    ##  mode        I2C|IIC, SPI, IO

    def setOperationMode(self, mode):

        self._sendCommand('+MODE ' + mode)
        result = self._readResponse()

        return result

    def getOperationMode(self):

        self._sendCommand('+MODE ?')
        result = self._readResponse()

        return result

    def setNumericalBase(self, base):

        self._sendCommand('+BASE ' + str(base))
        result = self._readResponse()

        return result

    def getNumericalBase(self):

        self._sendCommand('+BASE ?')
        result = self._readResponse()

        return result

    def setLEDRGB(self, red, green, blue):

        self._sendCommand('+LED ' + str(red) + ' ' + str(green) + ' ' + str(blue))
        result = self._readResponse()

        return result

    def setLEDColor(self, color):

        self._sendCommand('+LED ' + color)
        result = self._readResponse()

        return result

    def getFirmwareVer(self):

        self._sendCommand('+FWVER')
        result = self._readResponse()

        return result

    def getHardwareVer(self):

        self._sendCommand('+HWVER')
        result = self._readResponse()

        return result

    def resetToBtldr(self):

        self._sendCommand('+BTLDR')
        result = self._readResponse()

        return result

    def reset(self):

        self._sendCommand('+RESET')
        result = self._readResponse()

        return result

    def getDeviceID(self):

        self._sendCommand('+ID')
        result = self._readResponse()

        return result

    ## BUFFER COMMANDS

    def clearBuffer(self):

        self._sendCommand('BUF0 CLEAR')
        result = self._readResponse()

        return result

    def addByteToBuffer(self, value):

        self._sendCommand('BUF0 ADD ' + str(value))
        result = self._readResponse()

        return result

    def readBuffer(self, numBytes):

        self._sendCommand('BUF0 READ ' + str(numBytes))
        result = self._readResponse()

        return result

    def writeToBuffer(self, startIndex, data):

        bufferData = ''

        for x in data:
            bufferData += ' ' + str(x)

        self._sendCommand('BUF0 WRITE ' + str(startIndex) + bufferData)
        result = self._readResponse()

        return result

    ## I2C COMMANDS

    def setI2CClock(self, clock):

        self._sendCommand('I2C0 CLK ' + str(clock))
        result = self._readResponse()

        return result

    def getI2CClock(self):

        self._sendCommand('I2C0 CLK ?')
        result = self._readResponse()

        return result

    def setI2CPullUpState(self, pullUpState):

        self._sendCommand('I2C0 PULL ' + str(pullUpState))
        result = self._readResponse()

        return result

    def getI2CPullUpState(self):

        self._sendCommand('I2C0 PULL ?')
        result = self._readResponse()

        return result

    def scanI2CBus(self):

        self._sendCommand('I2C0 SCAN')
        result = self._readResponse()

        return result

    def scanI2CAddr(self, address):

        self._sendCommand('I2C0 SCAN ' + str(address))
        result = self._readResponse()

        return result

    def writeI2C(self, address, startingRegister, data):

        dataPacket = ''

        for x in data:
            dataPacket += ' ' + str(x)

        self._sendCommand('I2C0 WRITE ' + str(address) + ' ' + str(startingRegister) + dataPacket)
        result = self._readResponse()

        return result

    def writeByteI2C(self, data):

        self._sendCommand('I2C0 WRITE ' + str(data))
        result = self._readResponse()

        return result

    def readByteI2C(self, address):

        self._sendCommand('I2C0 REQ ' + str(address) + ' 1')
        result = self._readResponse()

        return result

    def readBytesI2C(self, address, numBytes):

        self._sendCommand('I2C0 REQ ' + str(address) + ' ' + str(numBytes))
        result = self._readResponse()

        return result

    def readI2C(self, address, startingRegister, numBytes):

        self._sendCommand('I2C0 READ ' + str(address) + ' ' + str(startingRegister) + ' ' + str(numBytes))
        result = self._readResponse()

        return result

    def writeFromBufferI2C(self, numBytes):

        self._sendCommand('I2C0 WRITE BUF0 ' + str(numBytes))
        result = self._readResponse()

        return result

    def readToBufferI2C(self, address, numBytes):

        self._sendCommand('I2C0 READ ' + str(address) + ' BUF0 ' + str(numBytes))
        result = self._readResponse()

        return result

    def startI2C(self, address):

        self._sendCommand('I2C0 START ' + str(address))
        result = self._readResponse()

        return result

    def endI2C(self, repeat=False):

        if repeat == True:
            self._sendCommand('I2C0 END R')
        else:
            self._sendCommand('I2C0 END')

        result = self._readResponse()

        return result

    def setI2CSlaveAddress(self, address):

        self._sendCommand('I2C0 SLAVE ' + str(address))
        result = self._readResponse()

        return result

    def getI2CSlaveAddress(self):

        self._sendCommand('I2C0 SLAVE ?')
        result = self._readResponse()

        return result

    def getI2CSlaveRequestInterrupt(self):

        result = self.interruptCheck('!I2C0 SLAVE RQ')

        return result

    def clearI2CSlaveRequestInterrupt(self):

        self.interruptClear('!I2C0 SLAVE RQ')

    def getI2CSlaveReceiveInterrupt(self):

        result = self.interruptCheck('!I2C0 SLAVE RX')

        return result

    def clearI2CSlaveReceiveInterrupt(self):

        self.interruptClear('!I2C0 SLAVE RX')

    ## SPI COMMANDS

    def setSPIClock(self, clock):

        self._sendCommand('SPI0 CLK ' + str(clock))
        result = self._readResponse()

        return result

    def getSPIClock(self):

        self._sendCommand('SPI0 CLK ?')
        result = self._readResponse()

        return result

    def setSPIOrder(self, order):

        self._sendCommand('SPI0 ORDER ' + order)
        result = self._readResponse()

        return result

    def getSPIOrder(self):

        self._sendCommand('SPI0 ORDER ?')
        result = self._readResponse()

        return result

    def setSPIMode(self, mode):

        self._sendCommand('SPI0 MODE ' + str(mode))
        result = self._readResponse()

        return result

    def getSPIMode(self):

        self._sendCommand('SPI0 MODE ?')
        result = self._readResponse()

        return result

    def getSPICPOL(self):

        self._sendCommand('SPI0 CPOL ?')
        result = self._readResponse()

        return result

    def getSPICPHA(self):

        self._sendCommand('SPI0 CPHA ?')
        result = self._readResponse()

        return result

    def setSPIBitsPerTransfer(self, bits):

        self._sendCommand('SPI0 TXBITS ' + str(bits))
        result = self._readResponse()

        return result

    def getSPIBitsPerTransfer(self):

        self._sendCommand('SPI0 TXBITS ?')
        result = self._readResponse()

        return result

    def beginSPI(self):

        self._sendCommand('SPI0 BEGIN')
        result = self._readResponse()

        return result

    def transferSPI(self, data):

        self._sendCommand('SPI0 TXRX ' + str(data))
        result = self._readResponse()

        return result

    def transferBufferSPI(self, numBytes):
        self._sendCommand('SPI0 TXRX BUF0 ' + str(numBytes))
        result = self._readResponse()

        return result

    def endSPI(self):

        self._sendCommand('SPI0 END')
        result = self._readResponse()

        return result

    ## IO COMMANDS

    ## GET/SET IOpinMode
    ##
    ## parameters:
    ##  ioNumber    0, 1, 2, 3, 4
    ##  mode        DIN, DOUT, AIN, AOUT, TOUCH, PWM
    ##
    ##  Note that not all modes are available on all pins

    def setIOpinMode(self, ioNumber, mode):

        self._sendCommand('IO' + str(ioNumber) + ' MODE ' + mode)
        result = self._readResponse()

        return result

    def getIOpinMode(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' MODE ?')
        result = self._readResponse()

        return result

    ## GET/SET IOpinInterrupt
    ##
    ## parameters:
    ##  ioNumber    0, 1, 2, 3, 4
    ##  intMode     CHANGE|CHANGING, RISE|RISING, FALL|FALLING, NONE|OFF|0

    def setIOpinInterrupt(self, ioNumber, intMode):

        self._sendCommand('IO' + str(ioNumber) + ' INT ' + intMode)
        result = self._readResponse()

        return result

    def getIOpinInterrupt(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' INT ?')
        result = self._readResponse()

        return result

    ## GET/SET IOpinValue
    ##
    ## parameters:
    ##  ioNumber    0, 1, 2, 3, 4
    ##  value       0|LOW, 1|HIGH, x%, Volts

    def setIOpinValue(self, ioNumber, value):

        self._sendCommand('IO' + str(ioNumber) + ' VALUE ' + str(value))
        result = self._readResponse()

        return result

    def getIOpinValue(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' VALUE ?')
        result = self._readResponse()

        return result

    def getIOpinInterrupt(self, ioNumber):

        result = self.interruptCheck('!I0' + str(ioNumber))

        return result

    def clearIOpinInterrupt(self, ioNumber):

        self.interruptClear('!IO' + str(ioNumber))