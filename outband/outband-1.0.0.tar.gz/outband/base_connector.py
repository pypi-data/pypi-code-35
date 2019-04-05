import abc
import typing

class BaseConnector(metaclass=abc.ABCMeta):
	@staticmethod
	@abc.abstractmethod
	def probe(host:str) -> bool:
		pass

	@staticmethod
	@abc.abstractmethod
	def connect(host:str, username:typing.Optional[str], password:typing.Optional[str], preserve_temp_files:bool) -> None:
		pass
