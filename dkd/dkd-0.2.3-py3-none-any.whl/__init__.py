# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao : Decentralized instant messaging
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from .content import MessageType, Content
from .contents import TextContent, CommandContent, HistoryContent, ForwardContent
from .message import Envelope, Message, IMessageDelegate
from .transform import InstantMessage, SecureMessage, ReliableMessage
from .transform import IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate

name = "DaoKeDao"

__author__ = 'Albert Moky'

__all__ = [
    # DaoKeDao
    'MessageType', 'Content',
    'TextContent', 'CommandContent', 'HistoryContent', 'ForwardContent',
    'Envelope', 'Message', 'IMessageDelegate',
    # message transform
    'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'IInstantMessageDelegate', 'ISecureMessageDelegate', 'IReliableMessageDelegate',
]
