# -*- coding: utf-8 -*-
"""
api module
----------

Contains the general network interactions for net.
"""

# std imports
import re
import math
import threading
import subprocess

# package imports
import net

# local imports
from net.imports import ConnectionRefusedError, PermissionError

__all__ = [
    'peers'
]


# threading
LOCK = threading.Lock()
IP_REGEX = re.compile(r'\d+\.\d+\.\d\.\d+')


# cache
PEERS = None


def peers(refresh=False, groups=None, on_host=False, hubs_only=False):
    """
    Get a list of all peers on your network. This is a cached values since the
    call to graph the network can be long. You can also limit this search to
    only look for operating peers on the localhost which does not require the
    long network scan, just set the ``on_host`` kwarg to True.

    Hubs act as the centers for certain application events or processes. In some
    cases, you may only want to subscribe or communicate with hubs. You can
    specify this through the ``hubs_only`` kwarg.

    The initial call to this will hang for a few seconds. Under the hood, it is
    making a shell call to ``arp -a`` which will walk your network and find all
    hosts.

    Standard call to get the peers on your network.

    .. code-block:: python

        all_peers = net.peers()

    Only search for peers on local host and not on the network.

    .. code-block:: python

        all_peers = net.peers(on_host=True)

    Refresh all peers in the cache

    .. code-block:: python

        all_peers = net.peers(refresh=True)

    Refresh the cache with peers in group1

    .. code-block:: python

        all_peers = net.peers("group1", refresh=True)

    Refresh the cache with peers in group1 and 2

    .. code-block:: python

        all_peers = net.peers(["group1", "group2"], refresh=True)

    Refresh the cache with all of the hubs on the network regardless of group.

    .. code-block:: python

        all_peers = net.peers(hubs_only=True, refresh=True)

    Refresh the cache with only hubs in group1 and 2

    .. code-block:: python

        all_peers = net.peers(["group1", "group2"], hubs_only=True, refresh=True)

    :param refresh: Bool
    :param groups: str
    :param on_host: Bool
    :param hubs_only: Bool
    :return: {

      # Peers
      'peers': {
          b'MTkyLjE2OC4yLjI0OjMwMTAgLT4gTm9uZQ==': {
              'group': 'None',
              'host': '192.168.2.24',
              'port': 3010,
              'hub': False,
              'executable': path/to/executable,
              'user': username
          },
      },

      # Groups
      'None': [
          b'MTkyLjE2OC4yLjI0OjMwMTAgLT4gTm9uZQ=='
      ]
    }
    """
    if PEERS is None or refresh:
        get_peers(groups, on_host, hubs_only)

    return PEERS


def local_network():
    """
    Runs ``arp -a`` to get all hosts.

    :return: list of ip address on the local network
    """
    raw_output = bytes(subprocess.check_output('arp -a', shell=True)).decode('ascii')
    return IP_REGEX.findall(raw_output)


def find_peers_in_block(ips, groups=None, hubs_only=False):
    """
    Sniffs out peers in the defined group based on the list of ip's

    :param ips: list of ip addresses
    :param groups: the list of groups you'd like to filter with. Defaults to the
     same as the current peer.
    :return: List of peer addresses
    """
    global PEERS

    # pull in the local peer
    peer = net.Peer()

    if not groups:
        groups = [peer.group]

    # loop over all the addresses
    for address in ips:

        # loop over ports
        for port in peer.ports():

            # skip self
            if port == peer.port and address == peer.host:
                continue

            # generate the peer
            foreign_peer_id = peer.generate_id(port, address)

            try:
                # ping the peer and if it responds with the proper info,
                # register it. Shut off the logger for this so we dont spam
                # the console.
                net.LOGGER.disabled = True
                info = net.info(peer=foreign_peer_id, time_out=0.1)
                net.LOGGER.disabled = False

                # skip registering this if the info is already in the
                # registry.
                if info in PEERS['peers'].values():
                    continue

                # filter out peers that aren't in the groups requested.
                if info['group'] not in groups:
                    continue

                # filter out non-hubs if that is what was requested
                if hubs_only and not info['hub']:
                    continue

                # acquire the lock and register
                LOCK.acquire()

                # register with the general information per peer
                PEERS['peers'][foreign_peer_id] = info

                # register with the group registry
                group_registry = PEERS.setdefault(info['group'], [])
                group_registry.append(foreign_peer_id)

                # release the shared resource
                LOCK.release()

            except (PermissionError, ConnectionRefusedError, OSError):
                net.LOGGER.disabled = False


def get_peers(groups, on_host, hubs_only):
    """
    Get a list of all valid remote peers.

    :param groups: List of groups
    :param on_host: Search only localhost
    :param hubs_only: Get Hubs only
    :return: List of peer addresses
    """
    global PEERS
    PEERS = {
        'peers': {}
    }

    # get this peer for pinging
    peer = net.Peer()

    # create subnet
    network = [net.HOST_IP]
    if not on_host:
        network = local_network()

    # logging help
    total_hosts = len(network)
    total_ports = len(peer.ports())
    net.LOGGER.debug(
        "Calculated network sweep: {0} hosts X {1} ports = {2} pings".format(
            total_hosts, total_ports, total_hosts * total_ports
        )
    )

    # skip the threading integration if the environment does not call for it.
    if net.THREAD_LIMIT <= 0:
        return find_peers_in_block(network, groups, hubs_only)

    # calculate thread chunk. There should always be at least one thread chunk
    thread_chunks = max(int(math.ceil(total_hosts/net.THREAD_LIMIT)), 1)

    # loop over and spawn threads
    start = 0
    threads = []

    for chunk in range(0, net.THREAD_LIMIT):
        end = start + thread_chunks

        thread = threading.Thread(
            target=find_peers_in_block,
            args=(network[start:end], groups, hubs_only)
        )
        thread.setName("Network_Scanner_" + str(chunk))
        thread.daemon = True
        threads.append(thread)
        thread.start()

        start = end

    # wait for all worker threads to finish
    for thread in threads:
        thread.join()

    return PEERS
