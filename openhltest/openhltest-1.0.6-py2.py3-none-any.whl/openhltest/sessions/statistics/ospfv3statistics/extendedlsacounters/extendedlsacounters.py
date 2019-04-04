from openhltest_client.base import Base


class ExtendedLsaCounters(Base):
	"""Extended LSA counters.
	"""
	YANG_NAME = 'extended-lsa-counters'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"TxLinkLsa": "tx-link-lsa", "TxInterAreaRouterLsa": "tx-inter-area-router-lsa", "RxLinkLsa": "rx-link-lsa", "TxNssaLsa": "tx-nssa-lsa", "TxNetworkLsa": "tx-network-lsa", "RxInterAreaRouterLsa": "rx-inter-area-router-lsa", "TxAsExternalLsa": "tx-as-external-lsa", "RxNetworkLsa": "rx-network-lsa", "TxInterAreaPrefixLsa": "tx-inter-area-prefix-lsa", "RxIntraAreaPrefixLsa": "rx-intra-area-prefix-lsa", "RxNssaLsa": "rx-nssa-lsa", "RxInterAreaPrefixLsa": "rx-inter-area-prefix-lsa", "RxAsExternalLsa": "rx-as-external-lsa", "RxRouterLsa": "rx-router-lsa", "TxIntraAreaPrefixLsa": "tx-intra-area-prefix-lsa", "TxRouterLsa": "tx-router-lsa"}

	def __init__(self, parent):
		super(ExtendedLsaCounters, self).__init__(parent)

	@property
	def RxAsExternalLsa(self):
		"""Received external-LSAs. The number of external LSAs received by theemulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-as-external-lsa')
	@RxAsExternalLsa.setter
	def RxAsExternalLsa(self, value):
		return self._set_value('rx-as-external-lsa', value)

	@property
	def RxInterAreaPrefixLsa(self):
		"""Received inter-area-prefix LSAs. The number of inter-area-prefix LSAsreceived by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-inter-area-prefix-lsa')
	@RxInterAreaPrefixLsa.setter
	def RxInterAreaPrefixLsa(self, value):
		return self._set_value('rx-inter-area-prefix-lsa', value)

	@property
	def RxInterAreaRouterLsa(self):
		"""Received inter-area-router LSAs. The number of inter-area-router LSAsreceived by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-inter-area-router-lsa')
	@RxInterAreaRouterLsa.setter
	def RxInterAreaRouterLsa(self, value):
		return self._set_value('rx-inter-area-router-lsa', value)

	@property
	def RxIntraAreaPrefixLsa(self):
		"""Received Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs receivedby the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-intra-area-prefix-lsa')
	@RxIntraAreaPrefixLsa.setter
	def RxIntraAreaPrefixLsa(self, value):
		return self._set_value('rx-intra-area-prefix-lsa', value)

	@property
	def RxLinkLsa(self):
		"""Received link-LSAs. The number of link LSAs received by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-link-lsa')
	@RxLinkLsa.setter
	def RxLinkLsa(self, value):
		return self._set_value('rx-link-lsa', value)

	@property
	def RxNetworkLsa(self):
		"""Received Network-LSAs - Number of Network LSAs received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-network-lsa')
	@RxNetworkLsa.setter
	def RxNetworkLsa(self, value):
		return self._set_value('rx-network-lsa', value)

	@property
	def RxNssaLsa(self):
		"""Received Link-LSAs. The number of Link LSAs received by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-nssa-lsa')
	@RxNssaLsa.setter
	def RxNssaLsa(self, value):
		return self._set_value('rx-nssa-lsa', value)

	@property
	def RxRouterLsa(self):
		"""Received Router-LSAs - Number of Router LSAs received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-router-lsa')
	@RxRouterLsa.setter
	def RxRouterLsa(self, value):
		return self._set_value('rx-router-lsa', value)

	@property
	def TxAsExternalLsa(self):
		"""Sent external-LSAs. The number of external LSAs sent by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-as-external-lsa')
	@TxAsExternalLsa.setter
	def TxAsExternalLsa(self, value):
		return self._set_value('tx-as-external-lsa', value)

	@property
	def TxInterAreaPrefixLsa(self):
		"""Sent inter-area-prefix LSAs. The number of inter-area-prefix LSAs sent bythe emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-inter-area-prefix-lsa')
	@TxInterAreaPrefixLsa.setter
	def TxInterAreaPrefixLsa(self, value):
		return self._set_value('tx-inter-area-prefix-lsa', value)

	@property
	def TxInterAreaRouterLsa(self):
		"""Sent inter-area-router LSAs. The number of inter-area-router LSAs sent bythe emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-inter-area-router-lsa')
	@TxInterAreaRouterLsa.setter
	def TxInterAreaRouterLsa(self, value):
		return self._set_value('tx-inter-area-router-lsa', value)

	@property
	def TxIntraAreaPrefixLsa(self):
		"""Sent Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs sent by theemulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-intra-area-prefix-lsa')
	@TxIntraAreaPrefixLsa.setter
	def TxIntraAreaPrefixLsa(self, value):
		return self._set_value('tx-intra-area-prefix-lsa', value)

	@property
	def TxLinkLsa(self):
		"""Sent link-LSAs. The number of link LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-link-lsa')
	@TxLinkLsa.setter
	def TxLinkLsa(self, value):
		return self._set_value('tx-link-lsa', value)

	@property
	def TxNetworkLsa(self):
		"""Sent Network-LSAs - Number of Network LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-network-lsa')
	@TxNetworkLsa.setter
	def TxNetworkLsa(self, value):
		return self._set_value('tx-network-lsa', value)

	@property
	def TxNssaLsa(self):
		"""Sent NSSA-LSAs. The number of NSSA LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-nssa-lsa')
	@TxNssaLsa.setter
	def TxNssaLsa(self, value):
		return self._set_value('tx-nssa-lsa', value)

	@property
	def TxRouterLsa(self):
		"""Sent Router-LSAs - Number of Router LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-router-lsa')
	@TxRouterLsa.setter
	def TxRouterLsa(self, value):
		return self._set_value('tx-router-lsa', value)

	def update(self, RxAsExternalLsa=None, RxInterAreaPrefixLsa=None, RxInterAreaRouterLsa=None, RxIntraAreaPrefixLsa=None, RxLinkLsa=None, RxNetworkLsa=None, RxNssaLsa=None, RxRouterLsa=None, TxAsExternalLsa=None, TxInterAreaPrefixLsa=None, TxInterAreaRouterLsa=None, TxIntraAreaPrefixLsa=None, TxLinkLsa=None, TxNetworkLsa=None, TxNssaLsa=None, TxRouterLsa=None):
		"""Update the current instance of the `extended-lsa-counters` resource

		Args:
			RxAsExternalLsa (uint64): Received external-LSAs. The number of external LSAs received by theemulated router.
			RxInterAreaPrefixLsa (uint64): Received inter-area-prefix LSAs. The number of inter-area-prefix LSAsreceived by the emulated router.
			RxInterAreaRouterLsa (uint64): Received inter-area-router LSAs. The number of inter-area-router LSAsreceived by the emulated router.
			RxIntraAreaPrefixLsa (uint64): Received Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs receivedby the emulated router.
			RxLinkLsa (uint64): Received link-LSAs. The number of link LSAs received by the emulatedrouter.
			RxNetworkLsa (uint64): Received Network-LSAs - Number of Network LSAs received by the emulated router.
			RxNssaLsa (uint64): Received Link-LSAs. The number of Link LSAs received by the emulatedrouter.
			RxRouterLsa (uint64): Received Router-LSAs - Number of Router LSAs received by the emulated router.
			TxAsExternalLsa (uint64): Sent external-LSAs. The number of external LSAs sent by the emulatedrouter.
			TxInterAreaPrefixLsa (uint64): Sent inter-area-prefix LSAs. The number of inter-area-prefix LSAs sent bythe emulated router.
			TxInterAreaRouterLsa (uint64): Sent inter-area-router LSAs. The number of inter-area-router LSAs sent bythe emulated router.
			TxIntraAreaPrefixLsa (uint64): Sent Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs sent by theemulated router.
			TxLinkLsa (uint64): Sent link-LSAs. The number of link LSAs sent by the emulated router.
			TxNetworkLsa (uint64): Sent Network-LSAs - Number of Network LSAs sent by the emulated router.
			TxNssaLsa (uint64): Sent NSSA-LSAs. The number of NSSA LSAs sent by the emulated router.
			TxRouterLsa (uint64): Sent Router-LSAs - Number of Router LSAs sent by the emulated router.
		"""
		return self._update(locals())

