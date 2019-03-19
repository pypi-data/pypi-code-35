from openhltest_client.base import Base


class Payload(Base):
	"""TBD
	"""
	YANG_NAME = 'payload'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Length": "length", "Repeat": "repeat", "Data": "data"}

	def __init__(self, parent):
		super(Payload, self).__init__(parent)

	@property
	def Data(self):
		"""TBD

		Returns:
			string

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('data')
	@Data.setter
	def Data(self, value):
		return self._set_value('data', value)

	@property
	def Repeat(self):
		"""Repeat the payload data to fill the length specified

		Returns:
			boolean

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('repeat')
	@Repeat.setter
	def Repeat(self, value):
		return self._set_value('repeat', value)

	@property
	def Length(self):
		"""TBD

		Returns:
			int32

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('length')
	@Length.setter
	def Length(self, value):
		return self._set_value('length', value)

	def update(self, Data=None, Repeat=None, Length=None):
		"""Update the current instance of the `payload` resource

		Args:
			Data (string): TBD
			Repeat (boolean): Repeat the payload data to fill the length specified
			Length (int32): TBD
		"""
		return self._update(locals())

