import pytest
import anyio
import trio
import mock
from time import time

from trio_click.testing import CliRunner
from .mock_serf import stdtest
from .run import run
from distkv.client import ServerError

import logging
logger = logging.getLogger(__name__)

# This is a basic Trio test which we keep around to check that
# (a) the autojump clock works as advertised
# (b) we can use anyio.
@pytest.mark.trio
async def test_00_anyio_clock(autojump_clock):
    assert trio.current_time() == 0
    t = time()

    for i in range(10):
        start_time = trio.current_time()
        await anyio.sleep(i)
        end_time = trio.current_time()

        assert end_time - start_time == i
    assert time()-t < 1

@pytest.mark.trio
async def test_00_runner(autojump_clock):
    with pytest.raises(AssertionError):
        await run('--doesnotexist')
    await run('--doesnotexist', expect_exit=2)
    #await run('pdb','pdb')  # used for verifying that debugging works

@pytest.mark.trio
async def test_01_basic(autojump_clock):
    async with stdtest(args={'init':123}) as st:
        s, = st.s
        async with st.client() as c:
            assert (await c.request("get_value", path=())).value == 123

            r = await c.request("set_value", path=("foo"), value="hello", nchain=3)
            r = await c.request("set_value", path=("foo","bar"), value="baz", nchain=3)
            r = await c.request("get_value", path=())
            assert r.value == 123

            r = await c.request("get_value", path=("foo"))
            assert r.value == "hello"

            r = await c.request("get_value", path=("foo","bar"))
            assert r.value == "baz"

            r = await c.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
            del r['tock']
            assert r == {'nodes': {'test_0': 3}, 'known': {'test_0': ((1, 4),)}, 'missing': {}, 'remote_missing': {}, 'seq': 7}

            assert (await c.request("get_value", node="test_0", tick=1)).value == 123
            assert (await c.request("get_value", node="test_0", tick=2)).value == "hello"
            assert (await c.request("get_value", node="test_0", tick=3)).value == "baz"

            r = await c.request("set_value", path=(), value=1234, nchain=3)
            assert r.prev==123
            assert r.chain.tick == 4

            # does not yet exist
            with pytest.raises(ServerError):
                await c.request("get_value", node="test_0", tick=8)
            # has been superseded
            with pytest.raises(ServerError):
                await c.request("get_value", node="test_0", tick=1)
            # works
            assert (await c.request("get_value", node="test_0", tick=4)).value == 1234

            r = await c.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
            del r['tock']
            del r['seq']
            assert r == {'nodes': {'test_0': 4}, 'known': {'test_0': ((1, 5),)}, 'missing': {}, 'remote_missing': {}}

@pytest.mark.trio
async def test_02_cmd(autojump_clock):
    async with stdtest(args={'init':123}) as st:
        s, = st.s
        async with st.client() as c:
            assert (await c.request("get_value", path=())).value == 123

            r = await run("client","-p",s.port,"set","-v","hello","foo")
            r = await run("client","-p",s.port,"set","-ev","'baz'","foo","bar")

            r = await run("client","-p",s.port,"get")
            assert r.stdout == "123\n"

            r = await run("client","-p",s.port,"get", "foo")
            assert r.stdout == "'hello'\n"

            r = await run("client","-p",s.port,"get", "foo", "bar")
            assert r.stdout == "'baz'\n"

            r = await c.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
            del r['tock']
            assert r == {'nodes': {'test_0': 3}, 'known': {'test_0': ((1, 4),)}, 'missing': {}, 'remote_missing': {}, 'seq': 2}

            assert (await c.request("get_value", node="test_0", tick=1)).value == 123
            assert (await c.request("get_value", node="test_0", tick=2)).value == "hello"
            assert (await c.request("get_value", node="test_0", tick=3)).value == "baz"

            r = await c.request("set_value", path=(), value=1234, nchain=3)
            assert r.prev==123
            assert r.chain.tick == 4

            # does not yet exist
            with pytest.raises(ServerError):
                await c.request("get_value", node="test_0", tick=8)
            # has been superseded
            with pytest.raises(ServerError):
                await c.request("get_value", node="test_0", tick=1)
            # works
            assert (await c.request("get_value", node="test_0", tick=4)).value == 1234

            r = await c.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
            del r['tock']
            del r['seq']
            assert r == {'nodes': {'test_0': 4}, 'known': {'test_0': ((1, 5),)}, 'missing': {}, 'remote_missing': {}}

@pytest.mark.trio
async def test_03_three(autojump_clock):
    async with stdtest(test_1={'init':125}, n=2, tocks=30) as st:
        s,si = st.s
        async with st.client(1) as ci:
            assert (await ci.request("get_value", path=())).value == 125

            r = await ci.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
            del r['tock']
            del r['seq']
            # Various stages of integrating test_0
            assert \
                r == {'nodes': {'test_1': 1}, 'known': {'test_1': (1,)}, 'missing': {}, 'remote_missing': {}} or \
                r == {'nodes': {'test_0': None, 'test_1': 1}, 'known': {'test_1': (1,)}, 'missing': {}, 'remote_missing': {}} or \
                r == {'nodes': {'test_0': None, 'test_1': 1}, 'known': {'test_1': (1,)}, 'missing': {'test_0': (1,)}, 'remote_missing': {'test_0': (1,)}} or \
                r == {'nodes': {'test_1': 1, 'test_0': None,}, 'known': {'test_0': (1,), 'test_1': (1,)}, 'missing': {}, 'remote_missing': {}} or \
                r == {'nodes': {'test_0': 0, 'test_1': 1}, 'known': {'test_1': (1,)}, 'missing': {}, 'remote_missing': {}} or \
                False


            # This waits for test_0 to be fully up and running.
            async with st.client(0) as c:

                # At this point ci shall be fully integrated, and test_1 shall know this (mostly).
                r = await ci.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
                del r['tock']
                del r['seq']
                assert \
                        r == {'nodes': {'test_0': 0, 'test_1': 1}, 'known': {'test_1': (1,)}, 'missing': {}, 'remote_missing': {}} or \
                        r == {'nodes': {'test_0': None, 'test_1': 1}, 'known': {'test_1': (1,)}, 'missing': {}, 'remote_missing': {}} 

                assert (await c.request("get_value", path=())).value == 125

                r = await c.request("set_value", path=(), value=126, nchain=3)
                assert r.prev==125
                assert r.chain.tick == 1
                assert r.chain.node == 'test_0'
                assert r.chain.prev.tick == 1
                assert r.chain.prev.node == 'test_1'
                assert r.chain.prev.tick == 1

                # This verifies that the chain entry for the initial update is gone
                # and the initial change is no longer retrievable.
                # We need the latter to ensure that there are no memory leaks.
                await anyio.sleep(1)
                r = await ci.request("set_value", path=(), value=127, nchain=3)
                assert r.prev==126
                assert r.chain.tick == 2
                assert r.chain.node == 'test_1'
                assert r.chain.prev.tick == 1
                assert r.chain.prev.node == 'test_0'
                assert r.chain.prev.tick == 1
                assert r.chain.prev.prev is None

                with pytest.raises(ServerError):
                    await c.request("get_value", node="test_1", tick=1)
                with pytest.raises(ServerError):
                    await ci.request("get_value", node="test_1", tick=1)
                
                # Now test that the internal states match.
                await anyio.sleep(1)
                r = await c.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
                del r['tock']
                del r['seq']
                assert r == {'nodes': {'test_0': 1, 'test_1': 2}, 'known': {'test_0': (1,), 'test_1': ((1,3),)}, 'missing': {}, 'remote_missing': {}}

            r = await ci.request("get_state", nodes=True, known=True, missing=True, remote_missing=True)
            del r['tock']
            del r['seq']
            assert r == {'nodes': {'test_0': 1, 'test_1': 2}, 'known': {'test_0': (1,), 'test_1': ((1,3),)}, 'missing': {}, 'remote_missing': {}}

