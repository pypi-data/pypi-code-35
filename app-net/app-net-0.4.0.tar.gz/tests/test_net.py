#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Tests for `net` package."""

# std imports
import traceback

# testing
import pytest

# package
import net


@pytest.fixture(scope="module")
def peers():
    """
    Set up the peers for testing.
    """
    net.LOGGER.debug("Test Header")

    master = net.Peer()
    slave = master.__class__(test=True)

    yield master, slave


def test_peer_construct(peers):
    """
    Construct and connect 2 peer servers.
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    assert master.port != slave.port
    assert not master.hub
    assert slave.ping(master.port, master.host) is True
    assert master.ping(slave.port, slave.host) is True

    with pytest.raises(RuntimeError):
        # this should fail so the user doesnt try to overwrite the running peer.
        net.peer._Peer()


def test_connect_decorator(peers):
    """
    Test the connect decorator
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    test_cases = [
        # dicts types
        {"testing": "value"}, {"1": 1}, {"1": {"2": 3}},

        # array types
        [1, "1", "1"], (1, 2, 3),

        # strings types
        "This is a string", "",

        # None type
        None,

        # bool types
        True, False,

        # number types
        1.0, 1,
    ]

    # loop over each test case and make sure a remote response equals to a local response.
    for case in test_cases:
        assert net.pass_through(case) == net.pass_through(case, peer=slave.id)

    # test that pass_through will allow both args and kwargs
    assert net.pass_through(
        "this",
        "is",
        a_test="case"
    ) == net.pass_through(
        "this",
        "is",
        a_test="case",
        peer=slave.id
    )

    # test the default handlers
    assert net.pass_through(master.get_flag('NULL')) == 'NULL'
    assert net.null() == "NULL"
    assert net.null(peer=slave.id) == "NULL"

    # test that connection requests work
    net.connections()
    net.connections(peer=slave.id)


def test_peer_handle(peers):
    """
    Tests that the peer is handling incoming requests correctly.
    """
    master, slave = peers

    try:
        master.request(slave.id, 'missing_connection', (), {})
        pytest.fail('Invalid connection is not being handled correctly.')
    except Exception as err:
        assert "Peer does not have the connection you are requesting" in traceback.format_exc()


def test_subscription(peers):
    """
    Tests the subscription system
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    assert slave.SUBSCRIPTIONS == {}

    @net.subscribe('test_event', peers=slave.id)
    def subscribe_test(test_case):
        return test_case

    assert slave.SUBSCRIPTIONS != {}

    @net.event('test_event')
    def event_test(*args, **kwargs):
        return args, kwargs

    event_test('testing')


def test_flag_decorator(peers):
    """
    Test the connect decorator
    """
    master, slave = peers

    # define the testing connection handler
    @net.connect()
    def test_response_handler():
        flag = net.Peer().get_flag("TEST")
        return flag

    # should throw an error since the flag is not defined yet
    with pytest.raises(Exception):

        net.LOGGER.disabled = True
        test_response_handler(peer=slave.id)
        net.LOGGER.disabled = False

    # define the missing flag
    @net.flag("TEST")
    def test_flag(connection, peer):
        return "TEST"

    # flag is defined and should not fail
    assert test_response_handler(peer=slave.id) == "TEST"


def test_api():
    """
    Test api functions
    """
    net.LOGGER.debug("Test Header")

    # test peer look up
    net.peers()
    net.peers(groups=['group1'], refresh=True)
    net.peers(on_host=True, refresh=True)

    # test non-threaded
    net.THREAD_LIMIT = 0

    net.peers()
    net.peers(groups=['group1'], refresh=True)
    net.peers(on_host=True, refresh=True)

    # test non-threaded
    net.THREAD_LIMIT = 5