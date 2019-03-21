from openhltest_client.base import Base


class IpVersion(Base):
	"""IP Version
	           IPV4 : IPv4
	           IPV6 : IPv6
	           BOTH : IPv4 and IPv6
	"""
	YANG_NAME = 'ip-version'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Single": "single", "PatternType": "pattern-type", "PatternFormat": "pattern-format", "ValueList": "value-list"}

	def __init__(self, parent):
		super(IpVersion, self).__init__(parent)

	@property
	def PatternFormat(self):
		"""Refine this leaf value with a regex of valid enum choices

		Returns:
			string

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('pattern-format')
	@PatternFormat.setter
	def PatternFormat(self, value):
		return self._set_value('pattern-format', value)

	@property
	def PatternType(self):
		"""TBD

		Returns:
			enumeration

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('pattern-type')
	@PatternType.setter
	def PatternType(self, value):
		return self._set_value('pattern-type', value)

	@property
	def Single(self):
		"""TBD

		Returns:
			string

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('single')
	@Single.setter
	def Single(self, value):
		return self._set_value('single', value)

	@property
	def ValueList(self):
		"""TBD

		Returns:
			string

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('value-list')
	@ValueList.setter
	def ValueList(self, value):
		return self._set_value('value-list', value)

	def update(self, PatternFormat=None, PatternType=None, Single=None, ValueList=None):
		"""Update the current instance of the `ip-version` resource

		Args:
			PatternFormat (string): Refine this leaf value with a regex of valid enum choices
			PatternType (enumeration): TBD
			Single (string): TBD
			ValueList (string): TBD
		"""
		return self._update(locals())

