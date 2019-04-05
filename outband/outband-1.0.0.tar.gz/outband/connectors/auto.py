import enum
import typing

import outband.base_connector
import outband.connectors.drac6

class Auto(outband.base_connector.BaseConnector):
	@staticmethod
	def probe(host:str) -> bool:
		raise Exception("Auto connector does not support probing.")

	@staticmethod
	def connect(host:str, username:typing.Optional[str], password:typing.Optional[str], preserve_temp_files:bool) -> None:
		matching_connectors = [connector for connector in KVMType if connector != KVMType.AUTO and connector.value.probe(host)]
		if len(matching_connectors) != 1:
			raise SystemExit("Unable to determine the KVM type automatically. Please specify it manually.")
		connector = matching_connectors[0].value
		connector.connect(host, username, password, preserve_temp_files)

class KVMType(enum.Enum):
	AUTO = Auto
	DRAC6 = outband.connectors.drac6.DRAC6

	def __str__(self) -> str:
		return self.name.lower()
