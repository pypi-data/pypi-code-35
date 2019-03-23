# -*- coding: utf-8 -*-
"""
api module
----------

Contains the general network interactions for net.
"""

__all__ = [
    'peers'
]

# std imports
import re
import math
import threading
import subprocess

# package imports
import net

# local imports
from net.imports import ConnectionRefusedError, PermissionError


# threading
LOCK = threading.Lock()
IP_REGEX = re.compile(r'\d+\.\d+\.\d\.\d+')


# cache
PEERS = None


def peers(refresh=False, groups=None):
    """
    Get a list of all peers on your network. This is a cached values since the
    call to graph the network can be long.

    The initial call to this will hang for a few seconds. Under the hood, it is
    making a shell call to ``arp -a`` which will walk your network and find all
    hosts.

    Standard call to get the peers on your network.

    .. code-block:: python

        all_peers = net.peers()

    Refresh all peers in the cache

    .. code-block:: python

        all_peers = net.peers(refresh=True)

    Refresh the cache with peers in group1

    .. code-block:: python

        all_peers = net.peers("group1", refresh=True)

    :param refresh: Bool
    :param groups: str
    :return:
    """
    if PEERS is None or refresh:
        get_peers(groups)

    return PEERS


def local_network():
    """
    Runs ``arp -a`` to get all hosts.

    :return: list of ip address on the local network
    """
    raw_output = bytes(subprocess.check_output('arp -a', shell=True)).decode('ascii')
    return IP_REGEX.findall(raw_output)


def find_peers_in_block(ips, groups=None):
    """
    Sniffs out peers in the defined group based on the list of ip's

    :param ips: list of ip addresses
    :param groups: the list of groups you'd like to filter with. Defaults to the
     same as the current peer.
    :return: List of peer addresses
    """
    global PEERS

    if not groups:
        groups = [net.Peer().group]

    # loop over all the addresses
    for address in ips:

        # loop over ports
        for port in net.Peer().ports():

            # loop over ports
            for group in groups:

                # generate the peer
                foreign_peer_id = net.Peer().generate_id(port, address, group)
                if foreign_peer_id == net.Peer().id:
                    continue

                try:
                    # ping the peer and if it responds with the proper info,
                    # register it. Shut off the logger for this so we dont spam
                    # the console.

                    net.LOGGER.disabled = True
                    info = net.info(peer=foreign_peer_id, time_out=0.1)
                    net.LOGGER.disabled = False

                    LOCK.acquire()
                    PEERS[foreign_peer_id] = info
                    LOCK.release()
                except (PermissionError, ConnectionRefusedError, OSError):
                    net.LOGGER.disabled = False


def get_peers(groups=None):
    """
    Get a list of all valid remote peers.

    :param groups: List of groups
    :return: List of peer addresses
    """
    global PEERS
    PEERS = {}

    # get this peer for pinging
    peer = net.Peer()

    # groups
    if not groups:
        groups = [peer.group]

    # create subnet
    network = local_network()

    # logging help
    total_hosts = len(network)
    total_ports = len(peer.ports())
    total_threads = net.THREAD_LIMIT
    net.LOGGER.debug(
        "Calculated network sweep: {0} hosts X {1} ports = {2} pings".format(
            total_hosts, total_ports, total_hosts * total_ports
        )
    )

    # skip the threading integration if the environment does not call for it.
    if total_threads <= 0:
        return find_peers_in_block(network, groups)

    # calculate thread chunk
    thread_chunks = int(math.ceil(total_hosts/total_threads))

    # loop over and spawn threads
    start = 0
    threads = []

    for chunk in range(0, total_threads):
        end = start + thread_chunks

        # spawn thread with network chunk calculated.
        thread = threading.Thread(
            target=find_peers_in_block,
            args=(network[start:end], groups)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

        start = end

    # wait for all worker threads to finish
    for thread in threads:
        thread.join()

    return PEERS
