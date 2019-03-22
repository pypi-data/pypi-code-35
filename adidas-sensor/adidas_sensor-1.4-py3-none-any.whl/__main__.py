#!python3

__author__ = 'Dipl.-Ing. Peter Blank'

########################################################################################################################################################################################################
#  !!! IMPORTANT: ONLY WORKING WITH PYTHON 3.X !!! #####################################################################################################################################################
# miPod read out script to get configuration and data ##################################################################################################################################################
# According to miPod_V1.3 firmware #####################################################################################################################################################################
########################################################################################################################################################################################################
# Imports
import os
import sys
import adidasSensor.serial as serial 






########################################################################################################################################################################################################
# Settings #############################################################################################################################################################################################
# files, commands and recieve strings ##################################################################################################################################################################
########################################################################################################################################################################################################
# Separator between data entries
seperator 			= ','
comma				= '.'

# File endings
fileEndingBin		= '.bin'
fileEndingConv 		= '.csv'

# Command paramter
cmdHeaderLen			= 3				# Length of command header: cmd byte + length byte + lineFeed byte = 3 bytes
cmdLen					= 61 			# Maximum length of command sequences: 61 bytes (USB transmit buffer is 64 bytes minus 3 bytes for header length)
cmdEnd	 				= 10 			# '\n' is 10 in decimal

# Sizes
dataLenData				= 2048			# USB receive buffer is 2048 bytes = size of 1 NAND flash page
dataLenConfig			= 48			# Size of transmitted configuration
dataLenCapacity			= 2				# Size of transmitted capacity
dataLenVoltage			= 2				# Size of transmitted voltage
dataLenUnique			= 8				# Size of transmitted unique id
dataLenAck				= 3				# Size of transmitted acknowledge command

pageLen					= 2048
acknowledge				= [0, 3, 10]	# First byte is cmd, second byte ist len, third byte is line feed






########################################################################################################################################################################################################
# miPod commands stored as dictionary ##################################################################################################################################################################
# "name" : [command interpretation by miPod, string value] #############################################################################################################################################
########################################################################################################################################################################################################
cmdDict = {
	'-c'		: [ 1, 'Print miPod sensor configuration [no params]'],
	'-r'		: [ 3, 'Reset miPod sensor configuration [no params]'],
	'-d'		: [ 2, 'Retrieve binary data and calibrate it with default values [no params]'],
	'-ef'		: [ 4, 'Erase NAND flash chip [no params]'],
	'-ut'		: [ 6, 'Update internal RTC time [no params]'],
	'-ud'		: [ 8, 'Update internal RTC date [no params]'],
	'-us'		: [ 7, 'Update IMU sampling rate [3.9,...,8000]Hz'],
	'-ua'		: [ 9, 'Update accelerometer range [2,4,8,16]g'],
	'-ug'		: [10, 'Update gyroscope range [250,500,1000,2000] /s'],
	'-id'		: [11, 'Update ID [4-digit hex number]'],
	'-cap'		: [12, 'Get current battery capacity [no params]'],
	'-volt'		: [13, 'Get current battery voltage [no params]'],
	'-ee'		: [14, 'Erase EEPROM chip [no params]'],
	'-mp'		: [15, 'Manipulate start page address [0,...,262143]'],
	'-u'		: [16, 'Transmit unique ID [no params]'],
	'-f'		: [17, 'Startup mesaurement [no params]'],
	'-df'		: [18, 'Stop startup measurement [no params]'],
	# Internal use only!
	'-ack'	: [ 0, '']
}
# Command dictionary paramters
cmdDictCmd		= 0
cmdDictString	= 1





########################################################################################################################################################################################################
# Conifguration structure stored as dictionary #########################################################################################################################################################
# "name" : [size in bytes (LSB is the first), position in the structure, value] ########################################################################################################################
########################################################################################################################################################################################################
configPacket = {
	### General settings
	'cfgLen'						: [1,   0, None, '[bytes]'],
	'batCap'						: [1,   1, None, '[mAh]'],
	'ID'							: [2,   2, None, '[4-digit hex number]'],
	###
	'HZ'							: [2,   4, None, '[Hz]'],
	'padding0'						: [2,   6, None, ''],
	'unique low'					: [4,   8, None, '[Unique ID low]'],
	'unique high'					: [4,  12, None, '[Unique ID high]'],
	
	### Measurement 1
	'accRange1'						: [1,  16, None, '[g]'],
	'gyroRange1'					: [1,  17, None, '[^/s]'],
	'HZ1'							: [2,  18, None, '[Hz]'],
	'dataPackets1'					: [4,  20, None, '[count]'],
	'dataPacketSize1'				: [4,  24, None, '[bytes]'],
	'dataPacketsPerPage1'			: [4,  28, None, '[count]'],
	'dataSizePerPage1'				: [4,  32, None, '[bytes]'],
	'startPage1'					: [4,  36, None, '[count]'],
	'pointerPage1'					: [4,  40, None, '[count]'],
	'startBlock1'					: [2,  44, None, '[count]'],
	'pointerBlock1'					: [2,  46, None, '[count]'],
}
# miPod configuration paramters
configPacketSize	= 0
configPacketPos		= 1	
configPacketValue	= 2
configPacketUnit	= 3






########################################################################################################################################################################################################
# Calucalte all possible sampling rates ################################################################################################################################################################
########################################################################################################################################################################################################
samplingRates = []
samplingRatesFiltered = []
for i in range(0,255,1):
	# if digital low pass filter is disabled: sr = (8000 / (regValue + 1))
	# else: sr = (1000 / (regValue + 1))
	samplingRates += [round((8000 / (i + 1)), 1)]
	samplingRatesFiltered += [round((1000 / (i + 1)), 1)]
samplingRates = sorted(list(set(samplingRates)))
samplingRatesFiltered = sorted(list(set(samplingRatesFiltered)))

def printSamplingRates(filtered):
	if filtered == True:
		list = samplingRatesFiltered
	else:
		list = samplingRates
	for i in range(0, len(list), 1):
		x = str(list[i])
		if len(x) == 6:
			x = '' + x + ' [Hz]'
		elif len(x) == 5:
			x = ' ' + x + ' [Hz]'
		elif len(x) == 4:
			x = '  ' + x + ' [Hz]'
		elif len(x) == 3:
			x = '   ' + x + ' [Hz]'
		elif len(x) == 2:
			x = '    ' + x + ' [Hz]'
		else:
			x = '     ' + x + ' [Hz]'
		print (x,  end = ' ')
		if ((i + 1) % 10) == 0:
			print ()
	print ()

	



########################################################################################################################################################################################################
# Calibration functions ################################################################################################################################################################################
########################################################################################################################################################################################################
def calibTempIMU(value):
	return round((value / 340) + 35, 2)
	
def calibCapLTC(value):
	# Magic battery capacity calibration constant :-) 0.890445
	return round(((value * 0.265625 * 0.890445) / configPacket['batCap'][configPacketValue]), 2)
	
def calibVoltLTC(value):
	return round((value * 6) / 65535, 2)

def calibAccXIMU(value):
	if configPacket['accRange1'][configPacketValue] == 2:
		x = 16384
	elif configPacket['accRange1'][configPacketValue] == 4:
		x = 8192
	elif configPacket['accRange1'][configPacketValue] == 8:
		x = 4096
	elif configPacket['accRange1'][configPacketValue] == 16:
		x = 2048
	else:
		x = 2048
	return round((value * 9.80665) / x, 4)

def calibAccYIMU(value):
	if configPacket['accRange1'][configPacketValue] == 2:
		x = 16384
	elif configPacket['accRange1'][configPacketValue] == 4:
		x = 8192
	elif configPacket['accRange1'][configPacketValue] == 8:
		x = 4096
	elif configPacket['accRange1'][configPacketValue] == 16:
		x = 2048
	else:
		x = 2048
	return round((value * 9.80665) / x, 4)

def calibAccZIMU(value):
	if configPacket['accRange1'][configPacketValue] == 2:
		x = 16384
	elif configPacket['accRange1'][configPacketValue] == 4:
		x = 8192
	elif configPacket['accRange1'][configPacketValue] == 8:
		x = 4096
	elif configPacket['accRange1'][configPacketValue] == 16:
		x = 2048
	else:
		x = 2048
	return round((value * 9.80665) / x, 4)

def calibGyroXIMU(value):
	if configPacket['gyroRange1'][configPacketValue] == 250:
		x = 131
	elif configPacket['gyroRange1'][configPacketValue] == 500:
		x = 65.5
	elif configPacket['gyroRange1'][configPacketValue] == 1000:
		x = 32.8
	elif configPacket['gyroRange1'][configPacketValue] == 2000:
		x = 16.4
	else:
		x = 16.4
	return round(value / x, 4)
	
def calibGyroYIMU(value):
	if configPacket['gyroRange1'][configPacketValue] == 250:
		x = 131
	elif configPacket['gyroRange1'][configPacketValue] == 500:
		x = 65.5
	elif configPacket['gyroRange1'][configPacketValue] == 1000:
		x = 32.8
	elif configPacket['gyroRange1'][configPacketValue] == 2000:
		x = 16.4
	else:
		x = 16.4
	return round(value / x, 4)

def calibGyroZIMU(value):
	if configPacket['gyroRange1'][configPacketValue] == 250:
		x = 131
	elif configPacket['gyroRange1'][configPacketValue] == 500:
		x = 65.5
	elif configPacket['gyroRange1'][configPacketValue] == 1000:
		x = 32.8
	elif configPacket['gyroRange1'][configPacketValue] == 2000:
		x = 16.4
	else:
		x = 16.4
	return round(value / x, 4)

def calibMagXIMU(value):
	return round(value * 0.3, 1)
	
def calibMagYIMU(value):
	return round(value * 0.3, 1)
	
def calibMagZIMU(value):
	return round(value * 0.3, 1)
	
def calibRTCTime(c, s, m, h):
	# order: centis / secs / mins / hours (encrypted in BCD format :-) have fun)
	centis = ((c >> 4) * 10) + (c & 0x0F)
	secs = ((((s & ~(1 << 7)) >> 4) * 10) + ((s & ~(1 << 7)) & 0x0F)) * 100
	mins = ((((m & ~(1 << 7)) >> 4) * 10) + ((m & ~(1 << 7)) & 0x0F)) * 100 * 60
	hours = ((((h & ~((1 << 7) | (1 << 6))) >> 4) * 10) + ((h & ~((1 << 7) | (1 << 6))) & 0x0F)) * 100 * 60 * 60
	return (centis + secs + mins + hours) 
	
def calibCentiSecRTC(value):
	# (encrypted in BCD format)
	return ((value >> 4) * 10) + (value & 0x0F)
	
def calibSecRTC(value):
	# (encrypted in BCD format)
	value &= ~(1 << 7)
	return ((value >> 4) * 10) + (value & 0x0F)
	
def calibMinRTC(value):
	# (encrypted in BCD format)
	value &= ~(1 << 7)
	return ((value >> 4) * 10) + (value & 0x0F)
	
def calibHourRTC(value):
	# (encrypted in BCD format)
	value &= ~((1 << 7) | (1 << 6))
	return ((value >> 4) * 10) + (value & 0x0F)
	
def calibPadding(value):
	return value

	




########################################################################################################################################################################################################
# Sensor data packet configuration as dictionary
# "name" : [sign, size in bytes (MSB is the first), position in the packet, calibration function]
########################################################################################################################################################################################################
sensorPacket = {
	'cnt'			: ['unsigned', 4,  0, calibPadding],
	'axImu'			: [  'signed', 2,  4, calibAccXIMU],
	'ayImu'			: [  'signed', 2,  6, calibAccYIMU],
	'azImu'			: [  'signed', 2,  8, calibAccZIMU],
	'tempImu'		: [  'signed', 2, 10, calibTempIMU],
	'gxImu'			: [  'signed', 2, 12, calibGyroXIMU],
	'gyImu'			: [  'signed', 2, 14, calibGyroYIMU],
	'gzImu'			: [  'signed', 2, 16, calibGyroZIMU],
	'mxImu'			: [  'signed', 2, 18, calibMagXIMU],
	'myImu'			: [  'signed', 2, 20, calibMagYIMU],
	'mzImu'			: [  'signed', 2, 22, calibMagZIMU],
	'rtc'			: ['unsigned', 4, 24, calibRTCTime],
	'cap'			: ['unsigned', 2, 28, calibCapLTC],
	'volt'			: ['unsigned', 2, 30, calibVoltLTC],
}
# miPod configuration paramters
sensorPacketSign	= 0
sensorPacketSize	= 1
sensorPacketPos		= 2
sensorPacketCalib	= 3		






########################################################################################################################################################################################################
# miPod class to read out the sensor
########################################################################################################################################################################################################
class MIPODReader:
	# Attributes
	__portName		= None
	__port 			= None
	__cmd 			= None
	__fileNameBin	= None
	__fileNameConv	= None
	__baudRate		= 115200	# in baud
	__timeOut		= 1			# in seconds
	__timeOutAck	= 25		# in seconds
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Constructor --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self, portName):
		self.__portName = str(portName)
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Open ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def openPort(self):
		# try:
		self.__port = serial.Serial(self.__portName, self.__baudRate, timeout = self.__timeOut) 
		# except:
		# 	print ('Cannot open port <' + self.__portName + '>!')
		# 	sys.exit(0)			
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Close opened port --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def closePort(self):
		# try:
		self.__port.close()
		# except:
		# 	print ('Cannot close port <' + self.__portName + '>!')
		# 	sys.exit(0)
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Convert binary data to integer -------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# rep = "usBig"    --> unsigned big endian
	# rep = "sBig"     --> signed big endian
	# rep = "usLittle" --> unsigned little endian
	# rep = "sLittle"  --> signed little endian
	def bytes2int(self, bytes, rep):
		if rep == 'usBig':
			return int.from_bytes(bytes, byteorder = 'big', signed = False)
		elif rep == 'sBig':
			return int.from_bytes(bytes, byteorder = 'big', signed = True)
		elif rep == 'usLittle':
			return int.from_bytes(bytes, byteorder = 'little', signed = False)
		elif rep == 'sLittle':
			return int.from_bytes(bytes, byteorder = 'little', signed = True)
		else:
			return 0
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Progress bar -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def progressBar(self, cur, max):
		percent = (int)((cur / max) * 100)
		print ('\rProgress: %-3d %s' % (percent, str('%')), end = '\r')
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Send command -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def sendCommand(self, cmd, data):
		# Create packet
		packet = bytearray()
		packet.append(cmd)
		if data == None:
			packet.append(cmdHeaderLen)
			packet.append(cmdEnd)
		else:
			packet.append(cmdHeaderLen + len(data))
			for i in range(0, len(data)):
				packet.append(data[i])
			packet.append(cmdEnd)
		# Try to send packet
		# try:
		self.__port.write(packet)
		# except:
		#	print ('ERROR in <sendCommand>: Cannot send command!')
		#	sys.exit(0)
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Retrieve data ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def retrieveData(self):
		# Try to retrieve data
		# try:
		data = self.__port.read(dataLenData)
		# except:
		#	print ('ERROR in <retrieveData>: Cannot retrieve data!')
		#	sys.exit(0)
		# No or not enough data retrevied
		if not len(data) == dataLenData:
			print ('ERROR in <retrieveData>: Wrong or no data!')
			print ('================================================================================')
			sys.exit(0)
		# Success
		return data
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Retrieve configuration ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def retrieveConfig(self):
		# Try to retrieve configuration
		# try:
		config = self.__port.read(dataLenConfig)
		# except:
		# 	print ('ERROR in <retrieveConfig>: Cannot retreive data!')
		# 	sys.exit(0)
		# No or not enough configuration data retrieved
		if not len(config) == dataLenConfig:
			print ('ERROR in <retrieveConfig>: Wrong or no configuration data!')
			print ('================================================================================')
			sys.exit(0)
		# Success
		return config
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Retrieve battery capacity ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def retrieveCapacity(self):
		# Try to retrieve capacity
		# try:
		capacity = self.__port.read(dataLenCapacity)
		# except:
		# 	print ('ERROR in <retrieveCapacity>: Cannot retreive data!')
		# 	sys.exit(0)
		# No or not enough capacity data retrieved
		if not len(capacity) == dataLenCapacity:
			print ('ERROR in <retrieveCapacity>: Wrong or no battery capacity data!')
			print ('================================================================================')
			sys.exit(0)
		# Success
		return self.bytes2int(capacity, 'usBig')
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Retrieve battery voltage -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def retrieveVoltage(self):
		# Try to retrieve voltage
		# try:
		voltage = self.__port.read(dataLenVoltage)
		# except:
		# 	print ('ERROR in <retrieveVoltage>: Cannot retreive data!')
		# 	sys.exit(0)
		# No or not enough voltage data retrieved
		if not len(voltage) == dataLenVoltage:
			print ('ERROR in <retrieveVoltage>: Wrong or no battery voltage data!')
			print ('================================================================================')
			sys.exit(0)
		# Success
		return self.bytes2int(voltage, 'usBig')
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Retrieve unique id -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def retrieveUnique(self):
		# Try to retrieve unique id
		# try:
		id = self.__port.read(8)
		# except:
		# 	print ('ERROR in <retrieveVoltage>: Cannot retreive data!')
		# 	sys.exit(0)
		# No or not enough voltage data retrieved
		if not len(id) == 8:
			print ('ERROR in <retrieveUnique>: Wrong or no unique id data!')
			print ('================================================================================')
			sys.exit(0)
		# Success
		return self.bytes2int(id, 'usBig')		
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Retrieve acknowledge -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def retrieveAck(self):
		# Set timeout for acknowledge
		self.__port.timeout = self.__timeOutAck
		# Try to retreive ack
		# try:
		ack = self.__port.read(dataLenAck)	
		# except:
		# 	self.__port.timeout = self.__timeOut
		# 	print ('ERROR in <retreiveAck>: Cannot retreive ack!')
		# 	sys.exit(0)
		# No or not enough data retrieved
		if not [int(i) for i in ack] == acknowledge:
			self.__port.timeout = self.__timeOut
			print ('ERROR in <retreiveAck>: Wrong or no acknowledge data!')
			print ('================================================================================')
			sys.exit(0)
		# Success
		self.__port.timeout = self.__timeOut
		return True
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Update local configuration -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def updateConfig(self, config):
		# Extract configuration, convert it and an put it into the configuration structure
		for key in sorted(configPacket.keys(), key = lambda x : configPacket[x][configPacketPos]):
			a = configPacket[key][configPacketPos]
			b = a + configPacket[key][configPacketSize]
			value = config[a:b]
			if 'accRange1' in key:
				value = self.bytes2int(value, 'usLittle')
				value = value >> 3
				if value == 0:
					value = 2
				elif value == 1:
					value = 4
				elif value == 2:
					value = 8
				elif value == 3:
					value = 16
				configPacket[key][configPacketValue] = value
			elif 'gyroRange1' in key:
				value = self.bytes2int(value, 'usLittle')
				value = value >> 3
				if value == 0:
					value = 250
				elif value == 1:
					value = 500
				elif value == 2:
					value = 1000
				elif value == 3:
					value = 2000
				configPacket[key][configPacketValue] = value
			elif key == 'ID':
				value = self.bytes2int(value, 'usLittle')
				id = hex(value).replace('0x', '').upper()
				for n in range(0, (4 - len(id))):
					id = '0' + id
				configPacket[key][configPacketValue] = id
			else:
				configPacket[key][configPacketValue] = self.bytes2int(value, 'usLittle')
		return True
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Execute specified command ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def execCommand(self, cmd, input):
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-c'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and get configuration data
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			config = self.retrieveConfig()
			# Update configuration structure
			self.updateConfig(config)
			# Print configuration structure in order
			print ('\n================================================================================')
			print   ('Current sensor configuration:')
			print ('================================================================================')
			for key in sorted(configPacket.keys(), key = lambda x : configPacket[x][configPacketPos]):
				if 'padding' in key:
					continue
				if '2' in key:
					continue
				if '3' in key:
					continue
				print ('%-20s = %-10s %-10s' % (key, configPacket[key][configPacketValue], configPacket[key][configPacketUnit]))
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-d'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and get configuration data first
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			config = self.retrieveConfig()
			# Update configuration structure
			self.updateConfig(config)
			# Set file names
			import time
			id = configPacket['ID'][configPacketValue]
			self.__fileNameBin 	= 'miPod_' + id + '__' + time.strftime('%d_%m__%Y_%H_%M', time.localtime()) + fileEndingBin
			self.__fileNameConv	= 'miPod_' + id + '__'+ time.strftime('%d_%m__%Y_%H_%M', time.localtime()) + fileEndingConv
			# Calculated expected amount of bytes
			amount = (configPacket['pointerPage1'][configPacketValue] - configPacket['startPage1'][configPacketValue]) * configPacket['dataSizePerPage1'][configPacketValue]
			step = configPacket['dataSizePerPage1'][configPacketValue]
			# Retrieve binary data 
			# try:
			file = open(self.__fileNameBin, 'ab')
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send acknowledge
			self.sendCommand(cmdDict['-ack'][cmdDictCmd], None)
			# # Read out dummy page
			# data = self.__port.read(configPacket['dataSizePerPage1'][configPacketValue])
			# self.__port.flushInput()
			# self.__port.flushOutput()
			# self.sendCommand(cmdDict['-ack'][cmdDictCmd], None)
			print ('\n================================================================================')
			print ('Retrieving binary data:')
			# Step through data page size wise
			for i in range(0, amount, step):
				self.progressBar(i, amount)
				data = self.__port.read(step)
				file.write(data)
				# Flush buffer
				self.__port.flushInput()
				self.__port.flushOutput()
				# Send acknowledge
				self.sendCommand(cmdDict['-ack'][cmdDictCmd], None)
			file.close()
			print ('\rProgress: %-3d %s' % (100, str('%')), end = '\r')
			print ('\nBinary data successfully retrieved!')
			# except:
			# print ('Cannot handle binary data for ' + self.__fileNameBin + '!')
			# sys.exit(0)
			# Convert binary data
			fileBin = open(self.__fileNameBin, 'rb')
			fileConv = open(self.__fileNameConv, 'a')
			#try:
			print ('================================================================================')
			print ('Converting binary data:')
			# Extract single sensor packets
			step = configPacket['dataPacketSize1'][configPacketValue]
			dataPackets = 0
			for j in range(0, amount, step):
				self.progressBar(j, amount)
				# All data has been converted
				if dataPackets == configPacket['dataPackets1'][configPacketValue]:
					break
				packet = fileBin.read(step)
				line = ''
				# Configuration of the sensor packet
				for key in sorted(sensorPacket.keys(), key = lambda x : sensorPacket[x][sensorPacketPos]):
					# Extract bytes of appropriate values 
					a = sensorPacket[key][sensorPacketPos]
					b = sensorPacket[key][sensorPacketPos] + sensorPacket[key][sensorPacketSize]
					bytes = packet[a:b]
					# Save counter for system packets
					if key == 'cnt':
						cntStr = str(self.bytes2int(bytes, 'usLittle'))
						line = line + cntStr + seperator
					# Save time stamp
					elif key == 'rtc':
						centis = self.bytes2int(bytes[0:1], 'usBig')
						secs = self.bytes2int(bytes[1:2], 'usBig')
						mins = self.bytes2int(bytes[2:3], 'usBig')
						hours = self.bytes2int(bytes[3:4], 'usBig')
						rtcStr = str(sensorPacket[key][sensorPacketCalib](centis, secs, mins, hours))
						line = line + rtcStr + seperator
					elif key == 'cap':
						capStr = str(sensorPacket[key][sensorPacketCalib](self.bytes2int(bytes, 'usBig')))
						line = line + capStr + seperator					
					elif key == 'volt':
						voltStr = str(sensorPacket[key][sensorPacketCalib](self.bytes2int(bytes, 'usBig')))
						line = line + voltStr + seperator
					elif key == 'mxImu':
						voltStr = str(sensorPacket[key][sensorPacketCalib](self.bytes2int(bytes, 'sLittle')))
						line = line + voltStr + seperator
					elif key == 'myImu':
						voltStr = str(sensorPacket[key][sensorPacketCalib](self.bytes2int(bytes, 'sLittle')))
						line = line + voltStr + seperator
					elif key == 'mzImu':
						voltStr = str(sensorPacket[key][sensorPacketCalib](self.bytes2int(bytes, 'sLittle')))
						line = line + voltStr + seperator
					# Normal IMU data
					else:
						dataStr = str(sensorPacket[key][sensorPacketCalib](self.bytes2int(bytes, 'sBig')))
						line = line + dataStr + seperator
				# Save data to file
				fileConv.write(line[:-1] + '\n')
				# Increase packet counter
				dataPackets = dataPackets + 1
			fileBin.close()
			fileConv.close()
			print ('\rProgress: %-3d %s' % (100, str('%')), end = '\r')
			print ('\nBinary data successfully converted!')
			print ('================================================================================')
			return True
			#except:
			#	print ('Cannot handle conversion for ' + self.__fileNameConv + ' !')
			#	sys.exit(0)
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-r'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and reset configuration data
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Reset sensor configuration ... ', end = '\r')	
			self.retrieveAck()
			print ('\rReset sensor configuration ... Success!')	
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-ef'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and erase flash chip
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Erase flash ... ', end = '\r')
			self.retrieveAck()
			print ('\rErase flash ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-ut'):
			# Get time and convert time to BCD format
			import time
			sec = (int)(time.localtime().tm_sec)
			sec = ((int)(sec / 10) << 4) + (sec % 10)
			min = (int)(time.localtime().tm_min)
			min = ((int)(min / 10) << 4) + (min % 10)
			hour = (int)(time.localtime().tm_hour)
			hour = ((int)(hour / 10) << 4) + (hour % 10)
			# Pack data to command
			data = bytearray()
			data.append(0)
			data.append(sec)
			data.append(min)
			data.append(hour)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and update time
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update internal RTC time ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate internal RTC time ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-ud'):
			# Get date and convert date to BCD format
			import time
			wday = (int)(time.localtime().tm_wday) + 1
			wday = ((int)(wday / 10) << 4) + (wday % 10)
			mday = (int)(time.localtime().tm_mday)
			mday = ((int)(mday / 10) << 4) + (mday % 10)
			mon = (int)(time.localtime().tm_mon)
			mon = ((int)(mon / 10) << 4) + (mon % 10)
			year = (int)(time.localtime().tm_year)
			cen = year // 100
			year = year - (100 * cen)
			year = ((int)(year / 10) << 4) + (year % 10)
			if cen == 20: 
				cen = 0
			elif cen == 21:
				cen = 1
			elif cen == 22:
				cen = 2
			elif cen == 23:
				cen = 3
			mon = mon | (cen << 6)
			# Pack data to command
			data = bytearray()
			data.append(wday)
			data.append(mday)
			data.append(mon)
			data.append(year)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and update time
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update internal RTC date ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate internal RTC date ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-us'):
			if input == None:
				print ()
				print ('No sampling rate set! Choose one of the following!')
				print ()
				print ('Digital low pass filter DISABLED:')
				printSamplingRates(False)
				print ()
				print ('Digital low pass filter ENABLED:')
				printSamplingRates(True)
				sys.exit(0)
			sr = float(input)
			if sr not in samplingRates:
				print ()
				print ('Wrong sampling rate! Choose one of the following!')
				print ()
				print ('Digital low pass filter DISABLED:')
				printSamplingRates(False)
				print ()
				print ('Digital low pass filter ENABLED:')
				printSamplingRates(True)
				sys.exit(0)
			sr = int(sr)
			# Pack data to command
			data = bytearray()
			data.append(sr & 0x00FF)
			data.append((sr >> 8) & 0x00FF)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and new sampling rate
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update sampling rate to ' + input + ' Hz ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate sampling rate to ' + input + ' Hz ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-ua'):
			if input == None:
				print ('No acceleromter range set!')
				sys.exit(0)
			accel = int(input)
			if accel not in [2,4,8,16]:
				print ('Wrong acceleromter range!')
				sys.exit(0)
			if accel == 2:
				accel = 0;
			elif accel == 4:
				accel = 1;
			elif accel == 8:
				accel = 2;
			elif accel == 16:
				accel = 3;
			# Pack data to command
			data = bytearray()
			data.append(accel & 0x03)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and new accelerometer range
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update accelerometer range to ' + str(input) + ' g ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate accelerometer range to ' + str(input) + ' g ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-ug'):
			if input == None:
				print ('No gyroscope range set!')
				sys.exit(0)
			gyro = int(input)
			if gyro not in [250,500,1000,2000]:
				print ('Wrong gyroscope range!')
				sys.exit(0)
			if gyro == 250:
				gyro = 0;
			elif gyro == 500:
				gyro = 1;
			elif gyro == 1000:
				gyro = 2;
			elif gyro == 2000:
				gyro = 3;
			# Pack data to command
			data = bytearray()
			data.append(gyro & 0x03)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and new gyroscope range
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update gyroscope range to ' + str(input) + ' °/s ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate gyroscope range to ' + str(input) + ' °/s ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-id'):
			if input == None:
				print ('No ID set!')
				sys.exit(0)
			if len(input) != 4:
				print ('ID must be a 4 digit hex number with leading zeros!')
				sys.exit(0)
			id = int(input, 16)
			# Pack data to command
			data = bytearray()
			data.append(id & 0x00FF)
			data.append((id >> 8) & 0x00FF)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and new sampling rate
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update ID to 0x' + input + ' ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate ID to 0x' + input + ' ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-cap'):
			# Flush buffer
			self.__port.flushInput()
			# Send command and get configuration data first
			self.sendCommand(cmdDict['-c'][cmdDictCmd], None)
			config = self.retrieveConfig()
			# Update configuration structure
			self.updateConfig(config)
			# Flush buffer
			self.__port.flushInput()
			# Send command and get capacity data
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			capacity = self.retrieveCapacity()
			# Print capacity
			capacity = calibCapLTC(capacity)
			print ('\n================================================================================')
			print ('Current battery capacity: ' + str(capacity) + ' [%]')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-volt'):
			# Flush buffer
			self.__port.flushInput()
			# Send command and get voltage data
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			voltage = self.retrieveVoltage()
			# Print voltage
			voltage = calibVoltLTC(voltage)
			print ('\n================================================================================')
			print ('Current battery voltage: ' + str(voltage) + ' [V]')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-u'):
			# Flush buffer
			self.__port.flushInput()
			# Send command and get voltage data
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			id = self.retrieveUnique()
			print ('\n================================================================================')
			print ('Unique id: ' + str(id) )
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-ee'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and erase eeprom chip
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Erase eeprom ... ', end = '\r')
			self.retrieveAck()
			print ('\rErase eeprom ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-f'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and erase eeprom chip
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Startup ... ', end = '\r')
			self.retrieveAck()
			print ('\Startup ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-df'):
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and erase eeprom chip
			self.sendCommand(cmdDict[cmd][cmdDictCmd], None)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Stop startup ... ', end = '\r')
			self.retrieveAck()
			print ('\Stop startup ... Success!')
			print ('================================================================================')
			return True
		# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if (cmd == '-mp'):
			if input == None:
				print ('No page address set!')
				sys.exit(0)
			page = int(input)
			if page < 0 or page > 262143:
				print ('Wrong page address range!')
				sys.exit(0)
			# Pack data to command
			data = bytearray()
			data.append((page >>  0) & 0xFF)
			data.append((page >>  8) & 0xFF)
			data.append((page >> 16) & 0xFF)
			data.append((page >> 24) & 0xFF)
			# Flush buffer
			self.__port.flushInput()
			self.__port.flushOutput()
			# Send command and new page address
			self.sendCommand(cmdDict[cmd][cmdDictCmd], data)
			# Wait for acknowledge
			print ('\n================================================================================')
			print ('Update page address to ' + input + ' ... ', end = '\r')
			self.retrieveAck()
			print ('\rUpdate page address to ' + input + ' ... Success!')
			print ('================================================================================')
			return True
			
			
			
	
########################################################################################################################################################################################################
# miPod class to read out the sensor ###################################################################################################################################################################
########################################################################################################################################################################################################
def main(args = sys.argv):
	flag = False
	if len(args) == 3:
		# Check command
		if not sys.argv[2] in cmdDict.keys():
			print ('Wrong command!')
			flag = True
		cmd = sys.argv[2]
		input = None
	elif len(args) == 4:
		# Check command
		if not sys.argv[2] in cmdDict.keys():
			print ('Wrong command or paramter!')
			flag = True
		cmd = sys.argv[2]
		input = sys.argv[3]
	else:
		flag = True
	if flag == True:
		print ('\n================================================================================')
		print   ('                      Welcome to the World of the miPod                         ')
		print ('================================================================================')
		print ('\nSpecify CDC port and command!')
		print ('Windows: COMXX  ---  Linux: /dev/ttyACMX  ---  Mac: /dev/tty.usbmodemXXX(X)\n')
		print ('Example: "py ' + str(sys.argv[0]) + ' COM75 -c"\n')
		print ('================================================================================')
		print ('Commands and paramter:')
		print ('================================================================================')
		for key in sorted(cmdDict.keys(), key = lambda x : cmdDict[x][cmdDictCmd]):
			if cmdDict[key][cmdDictString] == '':
				continue
			print ('   %-8s = %-5s' % (key, cmdDict[key][cmdDictString]))
		print ('================================================================================')
		sys.exit(0)
	# Create miPod reader
	miPod = MIPODReader(sys.argv[1])
	# Try to open CDC port
	miPod.openPort()
	# Execute command
	miPod.execCommand(cmd, input)
	# Try to close port
	miPod.closePort()
	
if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)