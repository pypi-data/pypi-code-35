from openhltest_client.base import Base


class Ospfv3Statistics(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/ospfv3-statistics resource.
	"""
	YANG_NAME = 'ospfv3-statistics'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'device-name'
	YANG_PROPERTY_MAP = {"TxLinkLsa": "tx-link-lsa", "RxInterAreaRouterLsa": "rx-inter-area-router-lsa", "RxUpdate": "rx-update", "TxHelloCount": "tx-hello-count", "RxRouterInfoLsa": "rx-router-info-lsa", "TxRouterInfoLsa": "tx-router-info-lsa", "RxNssaLsa": "rx-nssa-lsa", "TxInterAreaPrefixLsa": "tx-inter-area-prefix-lsa", "DeviceName": "device-name", "TxAck": "tx-ack", "RxLinkLsa": "rx-link-lsa", "RxDd": "rx-dd", "TxRequest": "tx-request", "RxNetworkLsa": "rx-network-lsa", "RxIntraAreaPrefixLsa": "rx-intra-area-prefix-lsa", "TxDd": "tx-dd", "TxNetworkLsa": "tx-network-lsa", "RxAck": "rx-ack", "TxAsExternalLsa": "tx-as-external-lsa", "TxInterAreaRouterLsa": "tx-inter-area-router-lsa", "RxRouterLsa": "rx-router-lsa", "RxInterAreaPrefixLsa": "rx-inter-area-prefix-lsa", "TxRouterLsa": "tx-router-lsa", "RouterState": "router-state", "RxRequest": "rx-request", "TxNssaLsa": "tx-nssa-lsa", "AdjacencyStatus": "adjacency-status", "TxUpdate": "tx-update", "RxAsExternalLsa": "rx-as-external-lsa", "PortName": "port-name", "TxIntraAreaPrefixLsa": "tx-intra-area-prefix-lsa", "RxHelloCount": "rx-hello-count"}

	def __init__(self, parent):
		super(Ospfv3Statistics, self).__init__(parent)

	@property
	def ExtendedLsaCounters(self):
		"""Extended LSA counters.

		Get an instance of the ExtendedLsaCounters class.

		Returns:
			obj(openhltest_client.openhltest.sessions.statistics.ospfv3statistics.extendedlsacounters.extendedlsacounters.ExtendedLsaCounters)
		"""
		from openhltest_client.openhltest.sessions.statistics.ospfv3statistics.extendedlsacounters.extendedlsacounters import ExtendedLsaCounters
		return ExtendedLsaCounters(self)._read()

	@property
	def DeviceName(self):
		"""An abstract test port name

		Getter Returns:
			string
		"""
		return self._get_value('device-name')

	@property
	def PortName(self):
		"""An abstract test port name

		Getter Returns:
			string
		"""
		return self._get_value('port-name')
	@PortName.setter
	def PortName(self, value):
		return self._set_value('port-name', value)

	@property
	def RouterState(self):
		"""Reports the state of adjacency on the current port.

		Getter Returns:
			DOWN | WAITING | DR | DR_OTHER | BACKUP
		"""
		return self._get_value('router-state')
	@RouterState.setter
	def RouterState(self, value):
		return self._set_value('router-state', value)

	@property
	def AdjacencyStatus(self):
		"""OSPFv2 Adjacency State.
		 DOWN    Initial state of a neighbor conversation. It indicates that therehas been no
		         recent information received from the neighbor.
		 ATTEMPT This state is only valid for neighbors attached to non-broadcastnetworks. It
		         indicates that no recent information has been received from theneighbor, but that
		         a more concerted effort should be made to contact the neighbor. This is done by
		         sending the neighbor Hello packets at intervals ofHelloInterval.
		
		 INIT    An Hello packet has recently been seen from the neighbor. However,bidirectional
		         communication has not yet been established with the neighbor(the router itself
		         did not appear in the neighbor's Hello packet). Allneighbors in this state (or higher)
		         are listed in the Hello packets sentfrom the associated interface.
		
		 TWOWAYS Communication between the two routers is bidirectional. This has been assured by the
		         operation of the Hello Protocol. This is the mostadvanced state short of beginning
		         adjacency establishment. The BackupDesignated Router (BDR) is selected from the set
		         of neighbors in the TWOWAYSstate or greater.
		
		 EXSTART This is the first step in creating an adjacency between the twoneighboring routers.
		         The goal of this step is to decide which router is the master, and to decide upon
		         the initial database description (DD) sequencenumber. Neighbor conversations in this
		         state or greater are calledadjacencies.
		
		 EXCHANGE In this state the router is describing its entire link statedatabase by sending
		         Database Description packets to the neighbor. EachDatabase Description Packet has
		         a DD sequence number, and is explicitlyacknowledged. Only one Database Description
		         Packet is allowed outstanding atany one time. In this state, Link State Request Packets
		         may also be sentasking for the neighbor's more recent advertisements. All adjacencies in
		         Exchange state or greater are used by the flooding procedure. In fact, these adjacencies
		         are fully capable of transmitting and receiving all types of OSPF routing protocol packets.
		         Loading Link State Request packets are sent to the neighbor asking for themore recent
		         advertisements that have been discovered (but not yet received)in the Exchange state.
		
		 FULL    Neighboring routers are fully adjacent. These adjacencies will nowappear in router
		         links and network links advertisements. 

		Getter Returns:
			DOWN | ATTEMPT | INIT | TWOWAYS | EXSTART | EXCHANGE | LOADING | FULL
		"""
		return self._get_value('adjacency-status')
	@AdjacencyStatus.setter
	def AdjacencyStatus(self, value):
		return self._set_value('adjacency-status', value)

	@property
	def TxHelloCount(self):
		"""Number of Hello packets transmitted by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-hello-count')
	@TxHelloCount.setter
	def TxHelloCount(self, value):
		return self._set_value('tx-hello-count', value)

	@property
	def RxHelloCount(self):
		"""Number of Hello packets received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-hello-count')
	@RxHelloCount.setter
	def RxHelloCount(self, value):
		return self._set_value('rx-hello-count', value)

	@property
	def RxAck(self):
		"""Received acks. The number of Link State Acknowledgment packets received by the emulated router. 

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-ack')
	@RxAck.setter
	def RxAck(self, value):
		return self._set_value('rx-ack', value)

	@property
	def RxDd(self):
		"""Received DD - The number of Database Description packets (containing LSAheaders) received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-dd')
	@RxDd.setter
	def RxDd(self, value):
		return self._set_value('rx-dd', value)

	@property
	def RxRequest(self):
		"""Received requests. The number of LS requests received by the emulatedrouter. 

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-request')
	@RxRequest.setter
	def RxRequest(self, value):
		return self._set_value('rx-request', value)

	@property
	def RxUpdate(self):
		"""Rx update.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-update')
	@RxUpdate.setter
	def RxUpdate(self, value):
		return self._set_value('rx-update', value)

	@property
	def RxRouterInfoLsa(self):
		"""The number of Router Information LSAs received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-router-info-lsa')
	@RxRouterInfoLsa.setter
	def RxRouterInfoLsa(self, value):
		return self._set_value('rx-router-info-lsa', value)

	@property
	def TxAck(self):
		"""Sent acks. The number of Link State Acknowledgment packets sent by theemulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-ack')
	@TxAck.setter
	def TxAck(self, value):
		return self._set_value('tx-ack', value)

	@property
	def TxDd(self):
		"""Sent DD - Number of Database Description packets sent by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-dd')
	@TxDd.setter
	def TxDd(self, value):
		return self._set_value('tx-dd', value)

	@property
	def TxRequest(self):
		"""Sent requests. The number of LS request packets sent by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-request')
	@TxRequest.setter
	def TxRequest(self, value):
		return self._set_value('tx-request', value)

	@property
	def TxUpdate(self):
		"""Tx update.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-update')
	@TxUpdate.setter
	def TxUpdate(self, value):
		return self._set_value('tx-update', value)

	@property
	def TxRouterInfoLsa(self):
		"""The number of Router Information LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-router-info-lsa')
	@TxRouterInfoLsa.setter
	def TxRouterInfoLsa(self, value):
		return self._set_value('tx-router-info-lsa', value)

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

	def create(self, DeviceName, PortName=None, RouterState=None, AdjacencyStatus=None, TxHelloCount=None, RxHelloCount=None, RxAck=None, RxDd=None, RxRequest=None, RxUpdate=None, RxRouterInfoLsa=None, TxAck=None, TxDd=None, TxRequest=None, TxUpdate=None, TxRouterInfoLsa=None, RxAsExternalLsa=None, RxInterAreaPrefixLsa=None, RxInterAreaRouterLsa=None, RxIntraAreaPrefixLsa=None, RxLinkLsa=None, RxNetworkLsa=None, RxNssaLsa=None, RxRouterLsa=None, TxAsExternalLsa=None, TxInterAreaPrefixLsa=None, TxInterAreaRouterLsa=None, TxIntraAreaPrefixLsa=None, TxLinkLsa=None, TxNetworkLsa=None, TxNssaLsa=None, TxRouterLsa=None):
		"""Create an instance of the `ospfv3-statistics` resource

		Args:
			DeviceName (string): An abstract test port name
			PortName (string): An abstract test port name
			RouterState (enumeration): Reports the state of adjacency on the current port.
			AdjacencyStatus (enumeration): OSPFv2 Adjacency State. DOWN    Initial state of a neighbor conversation. It indicates that therehas been no         recent information received from the neighbor. ATTEMPT This state is only valid for neighbors attached to non-broadcastnetworks. It         indicates that no recent information has been received from theneighbor, but that         a more concerted effort should be made to contact the neighbor. This is done by         sending the neighbor Hello packets at intervals ofHelloInterval. INIT    An Hello packet has recently been seen from the neighbor. However,bidirectional         communication has not yet been established with the neighbor(the router itself         did not appear in the neighbor's Hello packet). Allneighbors in this state (or higher)         are listed in the Hello packets sentfrom the associated interface. TWOWAYS Communication between the two routers is bidirectional. This has been assured by the         operation of the Hello Protocol. This is the mostadvanced state short of beginning         adjacency establishment. The BackupDesignated Router (BDR) is selected from the set         of neighbors in the TWOWAYSstate or greater. EXSTART This is the first step in creating an adjacency between the twoneighboring routers.         The goal of this step is to decide which router is the master, and to decide upon         the initial database description (DD) sequencenumber. Neighbor conversations in this         state or greater are calledadjacencies. EXCHANGE In this state the router is describing its entire link statedatabase by sending         Database Description packets to the neighbor. EachDatabase Description Packet has         a DD sequence number, and is explicitlyacknowledged. Only one Database Description         Packet is allowed outstanding atany one time. In this state, Link State Request Packets         may also be sentasking for the neighbor's more recent advertisements. All adjacencies in         Exchange state or greater are used by the flooding procedure. In fact, these adjacencies         are fully capable of transmitting and receiving all types of OSPF routing protocol packets.         Loading Link State Request packets are sent to the neighbor asking for themore recent         advertisements that have been discovered (but not yet received)in the Exchange state. FULL    Neighboring routers are fully adjacent. These adjacencies will nowappear in router         links and network links advertisements. 
			TxHelloCount (uint64): Number of Hello packets transmitted by the emulated router.
			RxHelloCount (uint64): Number of Hello packets received by the emulated router.
			RxAck (uint64): Received acks. The number of Link State Acknowledgment packets received by the emulated router. 
			RxDd (uint64): Received DD - The number of Database Description packets (containing LSAheaders) received by the emulated router.
			RxRequest (uint64): Received requests. The number of LS requests received by the emulatedrouter. 
			RxUpdate (uint64): Rx update.
			RxRouterInfoLsa (uint64): The number of Router Information LSAs received by the emulated router.
			TxAck (uint64): Sent acks. The number of Link State Acknowledgment packets sent by theemulated router.
			TxDd (uint64): Sent DD - Number of Database Description packets sent by the emulatedrouter.
			TxRequest (uint64): Sent requests. The number of LS request packets sent by the emulatedrouter.
			TxUpdate (uint64): Tx update.
			TxRouterInfoLsa (uint64): The number of Router Information LSAs sent by the emulated router.
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
		return self._create(locals())

	def read(self, DeviceName=None):
		"""Get `ospfv3-statistics` resource(s). Returns all resources from the server if `DeviceName` is not specified

		"""
		return self._read(DeviceName)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `ospfv3-statistics` resource

		"""
		return self._delete()

	def update(self, PortName=None, RouterState=None, AdjacencyStatus=None, TxHelloCount=None, RxHelloCount=None, RxAck=None, RxDd=None, RxRequest=None, RxUpdate=None, RxRouterInfoLsa=None, TxAck=None, TxDd=None, TxRequest=None, TxUpdate=None, TxRouterInfoLsa=None, RxAsExternalLsa=None, RxInterAreaPrefixLsa=None, RxInterAreaRouterLsa=None, RxIntraAreaPrefixLsa=None, RxLinkLsa=None, RxNetworkLsa=None, RxNssaLsa=None, RxRouterLsa=None, TxAsExternalLsa=None, TxInterAreaPrefixLsa=None, TxInterAreaRouterLsa=None, TxIntraAreaPrefixLsa=None, TxLinkLsa=None, TxNetworkLsa=None, TxNssaLsa=None, TxRouterLsa=None):
		"""Update the current instance of the `ospfv3-statistics` resource

		Args:
			PortName (string): An abstract test port name
			RouterState (enumeration): Reports the state of adjacency on the current port.
			AdjacencyStatus (enumeration): OSPFv2 Adjacency State. DOWN    Initial state of a neighbor conversation. It indicates that therehas been no         recent information received from the neighbor. ATTEMPT This state is only valid for neighbors attached to non-broadcastnetworks. It         indicates that no recent information has been received from theneighbor, but that         a more concerted effort should be made to contact the neighbor. This is done by         sending the neighbor Hello packets at intervals ofHelloInterval. INIT    An Hello packet has recently been seen from the neighbor. However,bidirectional         communication has not yet been established with the neighbor(the router itself         did not appear in the neighbor's Hello packet). Allneighbors in this state (or higher)         are listed in the Hello packets sentfrom the associated interface. TWOWAYS Communication between the two routers is bidirectional. This has been assured by the         operation of the Hello Protocol. This is the mostadvanced state short of beginning         adjacency establishment. The BackupDesignated Router (BDR) is selected from the set         of neighbors in the TWOWAYSstate or greater. EXSTART This is the first step in creating an adjacency between the twoneighboring routers.         The goal of this step is to decide which router is the master, and to decide upon         the initial database description (DD) sequencenumber. Neighbor conversations in this         state or greater are calledadjacencies. EXCHANGE In this state the router is describing its entire link statedatabase by sending         Database Description packets to the neighbor. EachDatabase Description Packet has         a DD sequence number, and is explicitlyacknowledged. Only one Database Description         Packet is allowed outstanding atany one time. In this state, Link State Request Packets         may also be sentasking for the neighbor's more recent advertisements. All adjacencies in         Exchange state or greater are used by the flooding procedure. In fact, these adjacencies         are fully capable of transmitting and receiving all types of OSPF routing protocol packets.         Loading Link State Request packets are sent to the neighbor asking for themore recent         advertisements that have been discovered (but not yet received)in the Exchange state. FULL    Neighboring routers are fully adjacent. These adjacencies will nowappear in router         links and network links advertisements. 
			TxHelloCount (uint64): Number of Hello packets transmitted by the emulated router.
			RxHelloCount (uint64): Number of Hello packets received by the emulated router.
			RxAck (uint64): Received acks. The number of Link State Acknowledgment packets received by the emulated router. 
			RxDd (uint64): Received DD - The number of Database Description packets (containing LSAheaders) received by the emulated router.
			RxRequest (uint64): Received requests. The number of LS requests received by the emulatedrouter. 
			RxUpdate (uint64): Rx update.
			RxRouterInfoLsa (uint64): The number of Router Information LSAs received by the emulated router.
			TxAck (uint64): Sent acks. The number of Link State Acknowledgment packets sent by theemulated router.
			TxDd (uint64): Sent DD - Number of Database Description packets sent by the emulatedrouter.
			TxRequest (uint64): Sent requests. The number of LS request packets sent by the emulatedrouter.
			TxUpdate (uint64): Tx update.
			TxRouterInfoLsa (uint64): The number of Router Information LSAs sent by the emulated router.
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

