# Tests for subcommands below 'create'
#  Ex: 'gracedb create emobservation'
import datetime
import pytest
import shlex
import six
try:
    from unittest import mock
except ImportError:
    import mock


###############################################################################
# Tests of individual subcommands #############################################
###############################################################################
def test_update_event_subcommand(CLI):
    """Test update event subcommand"""
    cmd_args = {
        'g_id': 'G1234',
        'filename': '/path/to/fake/file.xml',
    }

    # Generate command
    cmd = 'update event {g_id} {filename}'.format(**cmd_args)

    func = 'ligo.gracedb.rest.GraceDb.replaceEvent'
    with mock.patch(func) as mock_cli_func:
        CLI(shlex.split(cmd))

    # Check call count
    assert mock_cli_func.call_count == 1

    # Get args used in function call
    cli_args, cli_kwargs = mock_cli_func.call_args

    # Check args used in function call
    assert cli_args == (cmd_args['g_id'], cmd_args['filename'],)
    assert cli_kwargs == {}


SIGNOFF_TEST_DATA = [
    (None, None, None),
    ('FAKE_INSTRUMENT', 'FAKE_STATUS', 'test comment'),
]
@pytest.mark.parametrize("instrument,status,comment", SIGNOFF_TEST_DATA)
def test_update_signoff_subcommand(CLI, instrument, status, comment):
    """Test update signoff subcommand"""
    cmd_args = {
        's_id': 'S001122a',
        'signoff_type': 'FAKE_SIGNOFF_TYPE',
    }

    # Generate command
    cmd = "update signoff {s_id} {signoff_type}".format(**cmd_args)
    if instrument is not None:
        cmd += " {inst}".format(inst=instrument)
    if status is not None:
        cmd += " --status={status}".format(status=status)
    if comment is not None:
        cmd += " --comment='{comment}'".format(comment=comment)

    func = 'ligo.gracedb.rest.GraceDb.update_signoff'
    with mock.patch(func) as mock_cli_func:
        CLI(shlex.split(cmd))

    # Check call count
    assert mock_cli_func.call_count == 1

    # Get args used in function call
    cli_args, cli_kwargs = mock_cli_func.call_args

    # Check args used in function call
    assert cli_args == (cmd_args['s_id'], cmd_args['signoff_type'],)
    assert cli_kwargs == {'instrument': instrument or '', 'status': status,
        'comment': comment}


SUPEREVENT_TEST_DATA = [
    (None, None, None, None),
    (1, 2, 3, 'G1234'),
]
@pytest.mark.parametrize("t_start,t_0,t_end,pref_ev", SUPEREVENT_TEST_DATA)
def test_update_superevent_subcommand(CLI, t_start, t_0, t_end, pref_ev):
    """Test update superevent subcommand"""
    s_id = 'S001122a'

    # Generate command
    cmd = "update superevent {s_id}".format(s_id=s_id)
    if t_start is not None:
        cmd += " --t-start={ts}".format(ts=t_start)
    if t_0 is not None:
        cmd += " --t-0={t0}".format(t0=t_0)
    if t_end is not None:
        cmd += " --t-end={te}".format(te=t_end)
    if pref_ev is not None:
        cmd += " --preferred-event={pe}".format(pe=pref_ev)

    func = 'ligo.gracedb.rest.GraceDb.updateSuperevent'
    with mock.patch(func) as mock_cli_func:
        CLI(shlex.split(cmd))

    # Check call count
    assert mock_cli_func.call_count == 1

    # Get args used in function call
    cli_args, cli_kwargs = mock_cli_func.call_args

    # Check args used in function call
    assert cli_args == (s_id,)
    assert cli_kwargs == {'t_start': t_start, 't_0': t_0, 't_end': t_end,
        'preferred_event': pref_ev}
