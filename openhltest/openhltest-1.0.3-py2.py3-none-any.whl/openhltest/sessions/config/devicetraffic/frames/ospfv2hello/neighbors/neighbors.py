from openhltest_client.base import Base


class Neighbors(Base):
	"""TBD

	Implements the iterator interface __iter__ and encapsulates 0..n instances of the oht:sessions/config/device-traffic/frames/ospfv2-hello/neighbors resource.
	"""
	YANG_NAME = 'neighbors'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"Name": "name"}

	def __init__(self, parent):
		super(Neighbors, self).__init__(parent)

	@property
	def NeighborsId(self):
		"""Neighbor ID

		Get an instance of the NeighborsId class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicetraffic.frames.ospfv2hello.neighbors.neighborsid.neighborsid.NeighborsId)
		"""
		from openhltest_client.openhltest.sessions.config.devicetraffic.frames.ospfv2hello.neighbors.neighborsid.neighborsid import NeighborsId
		return NeighborsId(self)._read()

	@property
	def Name(self):
		"""TBD

		Returns:
			string

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('name')

	def create(self, Name):
		"""Create an instance of the `neighbors` resource

		Args:
			Name (string): TBD
		"""
		return self._create(locals())

	def read(self, Name=None):
		"""Get `neighbors` resource(s). Returns all resources from the server if `Name` is not specified

		"""
		return self._read(Name)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `neighbors` resource

		"""
		return self._delete()

