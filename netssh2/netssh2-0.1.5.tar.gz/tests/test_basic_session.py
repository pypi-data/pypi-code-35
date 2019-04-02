"""
Basic sanity test for SSH connection.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from netssh2.session import Session
import netssh2.exceptions as ex

HOST = "test.rebex.net"
USER = "demo"
PASSWD = "password"

NEWLINE = "\r\n"
PROMPT = "$ "

COMMAND = "uname"
OUTPUT = "Rebex Virtual Shell"


def get_session(**kwargs):
    """
    Creates instance of netssh2.session.Session object
    :param kwargs: any kwargs to pass to Session

    :return: session
    :rtype: class <netssh2.session.Session>
    """
    return Session(**kwargs)


class TestSSH(unittest.TestCase):
    """Basic SSH tests"""

    def test_blank_session(self):
        """Tests creating empty(default) session, should raise NetSsh2HostError exception"""
        with self.assertRaises(ex.NetSsh2HostError):
            get_session()

    def test_simple_ssh(self):
        """Tests creating and communicating over simple SSH."""
        session = get_session(host=HOST, user=USER, passwd=PASSWD)
        self.assertIsNotNone(session)
        self.assertEqual(session.run_cmd(COMMAND), 0)
        self.assertIn(OUTPUT, session.run_cmd(COMMAND, return_output=True)[1])
        self.assertTrue(session.disconnect())

    def test_invoke_shell_ssh(self):
        """Tests creating and communicating over simple SSH with invoke shell."""
        session = get_session(host=HOST, user=USER, passwd=PASSWD, invoke_shell=True, prompt=PROMPT, newline=NEWLINE)
        self.assertIsNotNone(session)
        self.assertEqual(session.run_cmd(COMMAND), 0)
        self.assertIn(OUTPUT, session.run_cmd(COMMAND, return_output=True)[1])
        self.assertTrue(session.disconnect())
