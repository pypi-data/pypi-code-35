from openhltest_client.base import Base


class Ports(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/device-traffic/ports resource.
	"""
	YANG_NAME = 'ports'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"RxFrames": "rx-frames", "RxFrameRate": "rx-frame-rate", "TxFrameRate": "tx-frame-rate", "Name": "name", "TxByteRate": "tx-byte-rate", "TxBitRate": "tx-bit-rate", "TxByteCount": "tx-byte-count", "RxByteCount": "rx-byte-count", "TxFrames": "tx-frames", "RxBitRate": "rx-bit-rate", "RxBitCount": "rx-bit-count", "DroppedFrames": "dropped-frames", "TxBitCount": "tx-bit-count", "RxByteRate": "rx-byte-rate"}

	def __init__(self, parent):
		super(Ports, self).__init__(parent)

	@property
	def Name(self):
		"""Port Streams name

		Getter Returns:
			string
		"""
		return self._get_value('name')

	@property
	def TxFrames(self):
		"""The total number of frames transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-frames')
	@TxFrames.setter
	def TxFrames(self, value):
		return self._set_value('tx-frames', value)

	@property
	def RxFrames(self):
		"""The total number of frames received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-frames')
	@RxFrames.setter
	def RxFrames(self, value):
		return self._set_value('rx-frames', value)

	@property
	def TxFrameRate(self):
		"""Total number of frames transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-frame-rate')
	@TxFrameRate.setter
	def TxFrameRate(self, value):
		return self._set_value('tx-frame-rate', value)

	@property
	def RxFrameRate(self):
		"""Total number of frames received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-frame-rate')
	@RxFrameRate.setter
	def RxFrameRate(self, value):
		return self._set_value('rx-frame-rate', value)

	@property
	def DroppedFrames(self):
		"""Total Number of dropped frames during transit.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('dropped-frames')
	@DroppedFrames.setter
	def DroppedFrames(self, value):
		return self._set_value('dropped-frames', value)

	@property
	def TxBitCount(self):
		"""The total number of bits transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-bit-count')
	@TxBitCount.setter
	def TxBitCount(self, value):
		return self._set_value('tx-bit-count', value)

	@property
	def RxBitCount(self):
		"""The total number of bits received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-bit-count')
	@RxBitCount.setter
	def RxBitCount(self, value):
		return self._set_value('rx-bit-count', value)

	@property
	def TxBitRate(self):
		"""Total number of bits transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-bit-rate')
	@TxBitRate.setter
	def TxBitRate(self, value):
		return self._set_value('tx-bit-rate', value)

	@property
	def RxBitRate(self):
		"""Total number of bits received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-bit-rate')
	@RxBitRate.setter
	def RxBitRate(self, value):
		return self._set_value('rx-bit-rate', value)

	@property
	def TxByteCount(self):
		"""The total number of bytes transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-byte-count')
	@TxByteCount.setter
	def TxByteCount(self, value):
		return self._set_value('tx-byte-count', value)

	@property
	def RxByteCount(self):
		"""The total number of bytes received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-byte-count')
	@RxByteCount.setter
	def RxByteCount(self, value):
		return self._set_value('rx-byte-count', value)

	@property
	def TxByteRate(self):
		"""Total number of bytes transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-byte-rate')
	@TxByteRate.setter
	def TxByteRate(self, value):
		return self._set_value('tx-byte-rate', value)

	@property
	def RxByteRate(self):
		"""Total number of bytes received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-byte-rate')
	@RxByteRate.setter
	def RxByteRate(self, value):
		return self._set_value('rx-byte-rate', value)

	def create(self, Name, TxFrames=None, RxFrames=None, TxFrameRate=None, RxFrameRate=None, DroppedFrames=None, TxBitCount=None, RxBitCount=None, TxBitRate=None, RxBitRate=None, TxByteCount=None, RxByteCount=None, TxByteRate=None, RxByteRate=None):
		"""Create an instance of the `ports` resource

		Args:
			Name (string): Port Streams name
			TxFrames (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxFrames (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			TxFrameRate (uint64): Total number of frames transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxFrameRate (uint64): Total number of frames received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			DroppedFrames (uint64): Total Number of dropped frames during transit.Empty if the abstract port is not connected to a test port.
			TxBitCount (uint64): The total number of bits transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxBitCount (uint64): The total number of bits received on the the port.Empty if the abstract port is not connected to a test port.
			TxBitRate (uint64): Total number of bits transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxBitRate (uint64): Total number of bits received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			TxByteCount (uint64): The total number of bytes transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxByteCount (uint64): The total number of bytes received on the the port.Empty if the abstract port is not connected to a test port.
			TxByteRate (uint64): Total number of bytes transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxByteRate (uint64): Total number of bytes received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
		"""
		return self._create(locals())

	def read(self, Name=None):
		"""Get `ports` resource(s). Returns all resources from the server if `Name` is not specified

		"""
		return self._read(Name)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `ports` resource

		"""
		return self._delete()

	def update(self, TxFrames=None, RxFrames=None, TxFrameRate=None, RxFrameRate=None, DroppedFrames=None, TxBitCount=None, RxBitCount=None, TxBitRate=None, RxBitRate=None, TxByteCount=None, RxByteCount=None, TxByteRate=None, RxByteRate=None):
		"""Update the current instance of the `ports` resource

		Args:
			TxFrames (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxFrames (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			TxFrameRate (uint64): Total number of frames transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxFrameRate (uint64): Total number of frames received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			DroppedFrames (uint64): Total Number of dropped frames during transit.Empty if the abstract port is not connected to a test port.
			TxBitCount (uint64): The total number of bits transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxBitCount (uint64): The total number of bits received on the the port.Empty if the abstract port is not connected to a test port.
			TxBitRate (uint64): Total number of bits transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxBitRate (uint64): Total number of bits received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			TxByteCount (uint64): The total number of bytes transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxByteCount (uint64): The total number of bytes received on the the port.Empty if the abstract port is not connected to a test port.
			TxByteRate (uint64): Total number of bytes transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxByteRate (uint64): Total number of bytes received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
		"""
		return self._update(locals())

