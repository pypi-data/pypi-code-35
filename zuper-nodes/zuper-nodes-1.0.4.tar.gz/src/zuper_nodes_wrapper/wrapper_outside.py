import json
import os
import time
from dataclasses import dataclass
from io import BufferedReader
from typing import *

from zuper_json.json_utils import encode_bytes_before_json_serialization
from zuper_nodes import InteractionProtocol
from zuper_nodes.compatibility import check_compatible_protocol
from zuper_nodes.structures import TimingInfo
from contracts import indent
from zuper_json.ipce import object_to_ipce, ipce_to_object
from zuper_json.json2cbor import read_next_either_json_or_cbor
from zuper_nodes_wrapper.meta_protocol import ProtocolDescription, basic_protocol
from . import logger, logger_interaction


def wait_for_creation(fn):
    while not os.path.exists(fn):
        msg = 'waiting for creation of %s' % fn
        logger.info(msg)
        time.sleep(1)


X = TypeVar('X')


@dataclass
class MsgReceived(Generic[X]):
    topic: str
    data: X
    timing: TimingInfo


from .constants import ENV_ENCODING, ENV_ENCODING_JSON, ENV_ENCODING_CBOR, TOPIC_ABORTED, FIELD_COMPAT, FIELD_TOPIC, \
    FIELD_DATA, FIELD_TIMING


def should_use_binary_encoding():
    encoding = os.environ.get(ENV_ENCODING, ENV_ENCODING_JSON)
    binary_out = ENV_ENCODING_CBOR == encoding
    return binary_out


import cbor2 as cbor

class RemoteNodeAborted(Exception):
    pass


class ComponentInterface(object):

    def __init__(self, fnin, fnout, expect_protocol: InteractionProtocol, nickname: str):
        self.nickname = nickname
        self._cc = None
        try:
            os.mkfifo(fnin)
        except BaseException as e:
            msg = f'Cannot create fifo {fnin}'
            raise Exception(msg) from e
        self.fpin = open(fnin, 'wb', buffering=0)
        wait_for_creation(fnout)
        self.fnout = fnout
        f = open(fnout, 'rb', buffering=0)
        # noinspection PyTypeChecker
        self.fpout = BufferedReader(f, buffer_size=1)
        self.nreceived = 0
        self.expect_protocol = expect_protocol
        self.node_protocol = None
        self.data_protocol = None
        # self._get_node_protocol()

    def close(self):
        self.fpin.close()
        self.fpout.close()

    def cc(self, f):
        """ CC-s everything that is read or written to this file. """
        self._cc = f

    def _get_node_protocol(self, timeout=None):
        self.write('wrapper.describe_protocol')
        ob: MsgReceived[ProtocolDescription] = self.read_one(expect_topic='protocol_description',
                                                             timeout=timeout)
        self.node_protocol = ob.data.data
        self.data_protocol = ob.data.meta

        if self.expect_protocol is not None:
            check_compatible_protocol(self.node_protocol, self.expect_protocol)

    def write(self, topic, data=None, with_schema=False, timing=None):
        suggest_type = None
        if self.node_protocol:
            if topic in self.node_protocol.inputs:
                suggest_type = self.node_protocol.inputs[topic]

        ipce = object_to_ipce(data,
                              {},
                              with_schema=with_schema,
                              suggest_type=suggest_type)

        # try to re-read
        if suggest_type:
            try:
                _ = ipce_to_object(ipce, {}, expect_type=suggest_type)
            except BaseException as e:
                msg = f'While attempting to write on topic "{topic}", cannot interpret the value as {suggest_type}.\nValue: {data}'
                raise Exception(msg) from e  # XXX

        msg = {FIELD_COMPAT: ['aido2'], FIELD_TOPIC: topic, FIELD_DATA: ipce, FIELD_TIMING: timing}

        j = self._serialize(msg)

        try:
            self.fpin.write(j)
            self.fpin.flush()
        except BrokenPipeError as e:
            msg = f'While attempting to write topic "{topic}" to node "{self.nickname}", I reckon that the pipe is closed and the node exited.'
            try:
                received = self.read_one(expect_topic=TOPIC_ABORTED)
                if received.topic == TOPIC_ABORTED:
                    msg += '\n\nThis is the aborted message:'
                    msg += '\n\n' + indent(received.data, ' |')
            except BaseException as e2:
                msg += f'\n\nI could not read any aborted message: {e2}'
            raise RemoteNodeAborted(msg) from e

        # make sure we write the schema when we copy it
        if not with_schema:
            msg[FIELD_DATA] = object_to_ipce(data, {}, with_schema=True)
            j = self._serialize(msg)

        if self._cc:
            self._cc.write(j)
            self._cc.flush()

        logger_interaction.info(f'Written to topic "{topic}" >> {self.nickname}.')

    def _serialize(self, msg) -> bytes:
        if should_use_binary_encoding():
            j = cbor.dumps(msg)
            return j
        else:
            msg = encode_bytes_before_json_serialization(msg)
            j = (json.dumps(msg) + '\n').encode('utf-8')
            return j

    def read_one(self, expect_topic=None, timeout=None) -> MsgReceived:
        try:
            if expect_topic:
                waiting_for = f'Expecting topic "{expect_topic}" << {self.nickname}.'
            else:
                waiting_for = None
            msg = read_next_either_json_or_cbor(self.fpout, timeout=timeout, waiting_for=waiting_for)
            # if self._cc:
            #     msg_b = self._serialize(msg)
            #     self._cc.write(msg_b)
            #     self._cc.flush()

            topic = msg[FIELD_TOPIC]
            if (expect_topic != TOPIC_ABORTED) and (topic == TOPIC_ABORTED):
                m = f'I was waiting for a message from component "{self.nickname}" but it aborted with the following error.'
                m += '\n\n' + indent(msg[FIELD_DATA], '|', f'{self.nickname} error |')
                raise RemoteNodeAborted(m)  # XXX

            if expect_topic:
                if topic != expect_topic:
                    msg = f'I expected topic "{expect_topic}" but received "{topic}".'
                    raise Exception(msg)  # XXX
            if topic in basic_protocol.outputs:
                klass = basic_protocol.outputs[topic]
            else:
                if self.node_protocol:
                    if topic not in self.node_protocol.outputs:
                        msg = f'Cannot find topic "{topic}" in outputs of detected node protocol.'
                        msg += '\nI know: %s' % sorted(self.node_protocol.outputs)
                        raise Exception(msg)  # XXX
                    else:
                        klass = self.node_protocol.outputs[topic]
                else:
                    if not topic in self.expect_protocol.outputs:
                        msg = f'Cannot find topic "{topic}".'
                        raise Exception(msg)  # XXX
                    else:
                        klass = self.expect_protocol.outputs[topic]
            data = ipce_to_object(msg[FIELD_DATA], {}, expect_type=klass)

            if self._cc:
                msg[FIELD_DATA] = object_to_ipce(data, {}, with_schema=True)
                msg_b = self._serialize(msg)
                self._cc.write(msg_b)
                self._cc.flush()

            timing = ipce_to_object(msg[FIELD_TIMING], {}, expect_type=TimingInfo)
            self.nreceived += 1
            return MsgReceived[klass](topic, data, timing)

        except StopIteration as e:
            msg = 'EOF detected on %s after %d messages.' % (self.fnout, self.nreceived)
            if expect_topic:
                msg += f' Expected topic "{expect_topic}".'
            raise StopIteration(msg) from e
        except TimeoutError as e:
            msg = 'Timeout detected on %s after %d messages.' % (self.fnout, self.nreceived)
            if expect_topic:
                msg += f' Expected topic "{expect_topic}".'
            raise TimeoutError(msg) from e
