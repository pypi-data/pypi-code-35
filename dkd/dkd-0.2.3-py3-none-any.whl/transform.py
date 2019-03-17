# -*- coding: utf-8 -*-
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

"""
    Message Transforming
    ~~~~~~~~~~~~~~~~~~~~

    Instant Message <-> Secure Message <-> Reliable Message
    +-------------+     +------------+     +--------------+
    |  sender     |     |  sender    |     |  sender      |
    |  receiver   |     |  receiver  |     |  receiver    |
    |  time       |     |  time      |     |  time        |
    |             |     |            |     |              |
    |  content    |     |  data      |     |  data        |
    +-------------+     |  key/keys  |     |  key/keys    |
                        +------------+     |  signature   |
                                           +--------------+
    Algorithm:
        data      = password.encrypt(content)
        key       = receiver.public_key.encrypt(password)
        signature = sender.private_key.sign(data)
"""

import json
from abc import abstractmethod

from .utils import base64_encode, base64_decode

from .content import Content
from .message import Envelope, Message, IMessageDelegate


def json_str(dictionary):
    """ convert a dict to json str """
    return json.dumps(dictionary)


def json_dict(string):
    """ convert a json str to dict """
    return json.loads(string)


class InstantMessage(Message):
    """
        Instant Message
        ~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content
            content  : {...}
        }
    """

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        # message content
        self.content = Content(msg['content'])
        return self

    @classmethod
    def new(cls, content: Content, envelope: Envelope=None,
            sender: str=None, receiver: str=None, time: int=0):
        if envelope:
            sender = envelope.sender
            receiver = envelope.receiver
            time = envelope.time
        # build instant message info
        msg = {
            'sender': sender,
            'receiver': receiver,
            'time': time,

            'content': content,
        }
        return InstantMessage(msg)

    def encrypt(self, password: dict, members: list=None):
        """
        Encrypt message content with password(symmetric key)

        :param password: A symmetric key for encrypting message content
        :param members:  If this is a group message, get all members here
        :return: SecureMessage object
        """
        msg = self.copy()

        # 1. encrypt 'content' to 'data'
        data = self.delegate.message_encrypt_content(msg=self, content=self.content, key=password)
        if data is None:
            raise AssertionError('failed to encrypt content with key: %s' % password)

        # 2. encrypt password to 'key'/'keys'
        if members is None:
            # personal message
            key = self.delegate.message_encrypt_key(msg=self, key=password, receiver=self.envelope.receiver)
            if key:
                msg['key'] = base64_encode(key)
            else:
                print('reused key for contact: %s' % self.envelope.sender)
        else:
            # group message
            keys = {}
            for member in members:
                key = self.delegate.message_encrypt_key(msg=self, key=password, receiver=member)
                if key:
                    keys[member] = base64_encode(key)
                else:
                    print('reused key for member: %s' % member)
            msg['keys'] = keys

        # 3. pack message
        msg['data'] = base64_encode(data)
        msg.pop('content')  # remove 'content'
        return SecureMessage(msg)


class SecureMessage(Message):
    """
        Secure Message
        ~~~~~~~~~~~~~~
        Instant Message encrypted by a symmetric key

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content data & key/keys
            data     : "...",  // base64_encode(symmetric)
            key      : "...",  // base64_encode(asymmetric)
            keys     : {
                "ID1": "key1", // base64_encode(asymmetric)
            }
        }
    """

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        # secure(encrypted) data
        self.data = base64_decode(msg['data'])
        # decrypt key/keys
        key = msg.get('key')
        keys = msg.get('keys')
        if key is not None:
            self.key = base64_decode(key)
            self.keys = None
        elif keys is not None:
            self.key = None
            self.keys = keys
        else:
            # reuse key/keys
            self.key = None
            self.keys = None
        return self

    # Group ID
    #    when a group message was split/trimmed to a single message,
    #    the 'receiver' will be changed to a member ID, and
    #    the 'group' will be set with the group ID.
    @property
    def group(self) -> str:
        return self.get('group')

    @group.setter
    def group(self, value):
        if value:
            self['group'] = value
        else:
            self.pop('group')

    @group.deleter
    def group(self):
        self.pop('group')

    def decrypt(self, member: str=None) -> InstantMessage:
        """
        Decrypt message data to plaintext content

        :param member: If this is a group message, give the member ID here
        :return: InstantMessage object
        """
        sender = self.envelope.sender
        receiver = self.envelope.receiver
        group = self.group

        # 0. check receiver/group member
        if member:
            # group message
            if group is None:
                # if field 'group' not exists, the receiver must be a group ID
                group = receiver
            else:
                # if field 'group' exists, it means this is a split message and
                # the receiver should be replaced to a member ID already,
                # but who knows...
                receiver = member
            # encrypted key
            if member in self.keys:
                key = self.keys[member]
            else:
                # trimmed?
                key = self.key
        else:
            # personal message
            key = self.key

        # 1. decrypt 'key' to symmetric key
        password = self.delegate.message_decrypt_key(msg=self, key=key, sender=sender, receiver=receiver, group=group)
        if password is None:
            raise AssertionError('failed to decrypt symmetric key: %s' % key)

        # 2. decrypt 'data' to 'content'
        content = self.delegate.message_decrypt_content(msg=self, data=self.data, key=password)
        if content is None:
            raise AssertionError('failed to decrypt message data: %s', self.data)

        # 3. pack message
        msg = self.copy()
        msg['content'] = content
        msg.pop('data')
        if 'key' in msg:
            msg.pop('key')
        if 'keys' in msg:
            msg.pop('keys')
        return InstantMessage(msg)

    def sign(self):
        """
        Sign the message.data with sender's private key

        :return: ReliableMessage object
        """

        # 1. sign message.data
        signature = self.delegate.message_sign(msg=self, data=self.data, sender=self.envelope.sender)
        if signature is None:
            raise AssertionError('failed to sign message: %s' % self)

        # 2. pack message
        msg = self.copy()
        msg['signature'] = base64_encode(signature)
        return ReliableMessage(msg)

    def split(self, members: list) -> list:
        """
        Split the group message to single person messages

        :param members: All group members
        :return:        A list of SecureMessage objects for all group members
        """
        msg = self.copy()
        keys = self.keys
        if 'keys' in msg:
            msg.pop('keys')
        else:
            keys = {}

        # 1. move the receiver(group ID) to 'group'
        msg['group'] = self.envelope.receiver

        messages = []
        for member in members:
            # 2. change receiver to each member
            msg['receiver'] = member
            # 3. get encrypted key
            if member in keys:
                msg['key'] = keys[member]
            elif 'key' in msg:
                msg.pop('key')
            # 4. pack message
            messages.append(SecureMessage(msg))
        # OK
        return messages

    def trim(self, member: str):
        """
        Trim the group message for a member

        :param member: Member ID
        :return:       A SecureMessage object drop all irrelevant keys to the member
        """
        msg = self.copy()

        # trim keys
        keys = msg.get('keys')
        if keys is not None:
            key = keys.get(member)
            if key is not None:
                msg['key'] = key
            msg.pop('keys')

        # msg['group'] = self.envelope.receiver
        # msg['receiver'] = member
        return SecureMessage(msg)


class ReliableMessage(SecureMessage):
    """
        This class is used to sign the SecureMessage
        It contains a 'signature' field which signed with sender's private key
    """

    def __new__(cls, msg: dict):
        self = super().__new__(cls, msg)
        # signature
        self.signature = base64_decode(msg['signature'])
        return self

    # Meta info of sender
    #    just for the first contact
    @property
    def meta(self) -> dict:
        return self.get('meta')

    @meta.setter
    def meta(self, value):
        if value:
            self['meta'] = value
        else:
            self.pop('meta')

    @meta.deleter
    def meta(self):
        self.pop('meta')

    def verify(self) -> SecureMessage:
        """
        Verify the message.data with signature

        :return: SecureMessage object if signature matched
        """
        data = self.data
        signature = self.signature
        sender = self.envelope.sender
        if self.delegate.message_verify(msg=self, data=data, signature=signature, sender=sender):
            msg = self.copy()
            msg.pop('signature')  # remove 'signature'
            return SecureMessage(msg)
        else:
            raise ValueError('Signature error')


#
#  Delegates
#


class IInstantMessageDelegate(IMessageDelegate):

    @abstractmethod
    def message_encrypt_content(self, msg: InstantMessage, content: Content, key: dict) -> bytes:
        """ Encrypt the message.content to message.data with symmetric key """
        pass

    @abstractmethod
    def message_encrypt_key(self, msg: InstantMessage, key: dict, receiver: str) -> bytes:
        """ Encrypt the symmetric key with receiver's public key """
        pass


class ISecureMessageDelegate(IMessageDelegate):

    @abstractmethod
    def message_decrypt_key(self, msg: SecureMessage, key: bytes, sender: str, receiver: str, group: str=None) -> dict:
        """ Decrypt key data to a symmetric key with receiver's private key """
        pass

    @abstractmethod
    def message_decrypt_content(self, msg: SecureMessage, data: bytes, key: dict) -> Content:
        """ Decrypt encrypted data to message.content with symmetric key """
        pass

    @abstractmethod
    def message_sign(self, msg: SecureMessage, data: bytes, sender: str) -> bytes:
        """ Sign the message data(encrypted) with sender's private key """
        pass


class IReliableMessageDelegate(IMessageDelegate):

    @abstractmethod
    def message_verify(self, msg: ReliableMessage, data: bytes, signature: bytes, sender: str) -> bool:
        """ Verify the message data and signature with sender's public key """
        pass
