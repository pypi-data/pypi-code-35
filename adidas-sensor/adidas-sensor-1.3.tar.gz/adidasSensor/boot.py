#!python3

__author__ = 'Dipl.-Ing. Peter Blank'

import adidasSensor.serial as serial
import os
import sys
import math





class EFM32_BOOTLOADER:
	"""
	Class handling Bootloader Functionality.
	"""
	### XMODEM-CRC SEND CONSTANTS ###
	SOH	= 0x01 														# Start of Header
	EOT	= 0x04 														# End of Transmission
	ETB	= 0x17 														# End of Transmission Block
	CAN	= 0x18 														# Cancelation
	### XMODEM-CRC RECEIVER CONSTANTS ###
	ACK	= bytearray([0x06]) 										# Acknowledge
	NAK	= bytearray([0x15]) 										# No Acknowledge
	CAC	= bytearray([0x43]) 										# Capital ANSII 'C' (Initiation)
	### BOOTLOADER CONSTANTS ###
	INFORMATION			= bytearray([0x69])							# Print Bootloader Version and Chip Unique ID
	UPLOAD_APPLICATION	= bytearray([0x75])							# Upload Application while keeping Bootloader intact
	UPLOAD_DESTRUCTIVE	= bytearray([0x64])							# Upload Application while overwriting Bootloader
	UPLOAD_USERPAGE		= bytearray([0x74])							# Write the User Information Page
	UPLOAD_LOCKPAGE		= bytearray([0x70])							# Write the Lock Bit Information Page
	BOOT_APPLICATION	= bytearray([0x62])							# Start the Application
	DEBUG_LOCK			= bytearray([0x6C])							# Set Debug Lock Bit in the User Page
	VERIFY_APPLICATION	= bytearray([0x63])							# Verify Application CRC-16 Checksum
	VERIFY_FLASH		= bytearray([0x76])							# Veriy Flash CRC-16 Checksum
	VERIFY_USERPAGE		= bytearray([0x6E])							# Verify User Page CRC-16 Checksum
	VERIFY_LOCKPAGE		= bytearray([0x6D])							# Verify Lock Page CRC-16 Checksum
	RESET				= bytearray([0x72])							# Reset the EFM32 Device
	### EFM32 SPECIFIC CONSTANTS ###
	BOOTLOADER_SIZE		= 0x00004000								# Size of Bootloader (16k <---> 16384 Bytes)
	FLASH_SIZE			= 0x00040000								# Size of Flash (256k <---> 262144 Bytes)
	### CYCLIC REDUNDANCY CHECK TABLE ###
	CRCTABLE = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
				0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
				0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
				0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
				0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
				0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
				0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
				0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
				0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
				0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
				0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
				0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
				0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
				0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
				0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
				0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
				0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
				0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
				0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
				0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
				0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
				0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
				0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
				0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
				0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
				0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
				0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
				0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
				0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
				0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
				0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
				0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0]
	# SERIAL PORT CONNECTION
	portName 	= None
	port		= None
	
	
	
	
	
	def __init__(self):
		"""
		Initialize Bootloader.
		"""
		pass
		
		
		
		
		
	def openSerialPort(self, _portName):
		"""
		Open specified serial Port <_portName>.
		"""
		self.portName = _portName
		self.port = serial.Serial(self.portName, timeout = 5, baudrate = 115200)
		
		
		
		
		
	def closeSerialPort(self):
		"""
		Close open serial Port.
		"""
		self.portName = None
		if self.port is not None:
			self.port.close()
			
			
			
			
			
	def getSerialPortName(self):
		"""
		Return serial Port Name.
		"""
		return self.portName
		
		
		
		
		
	def getCRC(self, _data, _crc = 0x00):
		""" 
		Calculate CRC-16 bit Checksum of Bytearray <_data>.
		"""
		for byte in _data:
			_crc = ((_crc << 0x08) & 0xFF00) ^ self.CRCTABLE[((_crc >> 0x08) & 0xFF) ^ byte]
		return (_crc & 0xFFFF)
		
		
		
		
		
	def getFileChecksum(self, _file):
		""" 
		Calculate CRC-16 bit Checksum of binary File <_file>.
		"""
		fileObject = open(_file, 'rb')										# Open Application File
		data = bytearray()													# Create Data Object
		cnt = 0x00															# Create Byte Counter
		end = False															# Termination Flag
		while end == False:													# Endless Loop until File is read
			byte = fileObject.read(1)										# Read Byte from File
			if not len(byte) == 0x01:										# Check for EOF
				paddingBytes = self.FLASH_SIZE - self.BOOTLOADER_SIZE - cnt	# Calculate Padding Bytes
				for i in range(0, paddingBytes):							# Add Padding Bytes
					data.append(0xFF)
				end = True													# Termination on
			else:															# No EOF
				cnt = cnt + 0x01											# Increment Byte Counter
				data = data + byte											# Add Data Byte
		fileObject.close()													# Close Application File
		return self.getCRC(data)											# Calculate CRC and return Checksum
		
		
		
		
		
	def getInfo(self):
		""" 
		Print Device Information String.
		"""
		self.port.write(self.INFORMATION)									# Send Bootloader Command
		self.port.flush()													# Flush Serial Port
		self.port.readline()												# Command Echo
		self.port.readline()												# Newline
		info = self.port.readline()[:-0x02].decode('utf-8')					# Get Response an convert to String
		print ('[INFO       ]\t%s' % info)
		return (info)
		
		
		
		
		
	def uploadApp(self, _file, _gProgressBar = None):
		""" 
		Upload Application inside binary File <_file>.
		"""
		self.port.write(self.UPLOAD_APPLICATION)							# Send Bootloader Command
		self.port.readline()												# Command Echo
		self.port.readline()												# 'Ready'
		if self.port.read() == self.CAC:									# Initiation
			print ('[INFO       ]\tStart Application Upload')
			k = 0															# Loop Counter
			size = 0														# File size 
			if _gProgressBar is not None:
				import time
				fileObject = open(_file, 'rb')
				fileObject.seek(0, os.SEEK_END)
				size = int(math.ceil(fileObject.tell() / 128))
				_gProgressBar.setMaximum(size)								# Set Maximum for the graphical Progress Bar
				fileObject.close()
			fileObject = open(_file, 'rb')
			i = 0x01														# Initialize Packet Number with 0x01
			end = False														# Termination Flag
			while end == False:												# Endless Loop until all Data is transmitted
				packet = bytearray()
				packet.append(self.SOH)
				packet.append(i)											# Append Packet Number
				packet.append(0xFF - i)										# Append Complementary Packet Number
				data = fileObject.read(128)									# Read 128 Byte Block from File
				if _gProgressBar is not None:
					_gProgressBar.updateBar(k)								# Update graphical Progress Bar
					#time.sleep(0.01)
				if not len(data) == 0x80:									# Check for EOF
					packet = packet + data									# Add remaining Data Bytes
					paddingBytes = 0x80 - len(data)							# Calculate Padding Bytes
					for i in range(0, paddingBytes):						# Add Padding Bytes
						packet.append(0xFF)
					end = True												# Termination on
				else:
					packet = packet + data									# Append Data Packet
				crc = self.getCRC(packet[3:131])							# Calculate CRC (only for Data Byte Block)
				packet.append(crc >> 0x08)									# Append high Byte of CRC-16
				packet.append(crc & 0xFF)									# Append low Byte of CRC-16
				self.port.write(packet)										# Send Packet
				self.port.flush()											# Flush Serial Port
				if self.port.read() == self.NAK:							# Check Acknowledge
					print ('[ERROR -SOH-]\tNo Acknowledge Detected')
					fileObject.close()
					return False
				i = (i + 0x01) % 0x0100										# Increase Packet Number (overflow at 0xFF)
				k = k + 1													# Increase Loop Counter
			self.port.write(bytes([self.EOT]))								# Send EOT
			if self.port.read() == self.NAK:								# Check Acknowledge
				print ('[ERROR -EOT-]\tNo Acknowledge Detected')
				# TODO Error Handling
				fileObject.close()
				return False
			crcFile = self.getFileChecksum(_file)							# Get File Checksum
			if _gProgressBar is not None:
				_gProgressBar.updateBar(size)								# Update graphical Progress Bar
			print ('[INFO       ]\tEnd Application Upload')
		else:																# Initiation failed
			print('[ERROR -CAC-]\tInitiation failed')
			fileObject.close()
			return False
		return True
		
		
		
		
		
	def verifyApp(self, _file, _gProgressBar = None):
		""" 
		Verify uploaded Application of binary File <file>.
		"""
		self.port.write(self.VERIFY_APPLICATION)							# Send Verification Command
		self.port.flush()													# Flush Serial Port
		self.port.readline()												# Command Echo
		if _gProgressBar is not None:
			self.showGraphicalProgressBar(_gProgressBar, 1)					# Show graphical Porgress
		crcApp = int(self.port.readline()[5:-2].decode('utf-8'), 16)		# Get Application Checksum and convert it
		crcFile = self.getFileChecksum(_file)								# Get File Checksum
		if crcApp == crcFile:												# Check CRC-16
			print ('[INFO       ]\tVerification Succeeded')
			return True
		else:
			print('[ERROR -CRC-]\tVerification Failed')
			return False
			
			
			
			
			
	def boot(self):
		""" 
		Boot Application.
		"""
		print ('[INFO       ]\tBoot Application in 7 Seconds')
		self.port.write(self.BOOT_APPLICATION)								# Send Bootloader Command
		self.port.flush()													# Flush Serial Port
		
		
		
		
		
	def reset(self):
		""" 
		Reset EFM32 Device.
		"""
		print ('[INFO       ]\tReset Microcontoller in 7 Seconds')
		self.port.write(self.RESET)											# Send Reset Command
		self.port.flush()													# Flush Serial Port
		
		
		
		
		
	def showGraphicalProgressBar(self, _gProgressBar, _time):
		"""
		Wait a certain Time <_time> in Seconds for user-friendly update Functionality using a graphical Progress Bar <_gProgressBar>.
		"""
		from time import sleep
		_gProgressBar.setMaximum(100)
		i = 0
		while i < _time:
			sleep(0.01)
			i = i + 0.01
			_gProgressBar.updateBar((int)((i / _time) * 100))
			
			
			
			
			
			
			
			
			
			
if __name__ == '__main__':
	"""
	Main Function to execute Bootloader as a Script and not as Module Import.
	"""
	if sys.argv[1] is '' or sys.argv[1] is None:
		print ('Specify Serial Port and File as Arguments!')
		print ('E.g.: python boot.py COM77 main.bin')
		sys.exit(0)
	loader = EFM32_BOOTLOADER()
	loader.openSerialPort(sys.argv[1])
	loader.getInfo()
	if sys.argv[2] == 'boot':
		pass
	else:
		loader.uploadApp(sys.argv[2])
		loader.verifyApp(sys.argv[2])
	loader.boot()
	loader.closeSerialPort()