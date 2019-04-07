import argparse
import inspect
import io
import json
import logging
import os
import socket
import stat
import sys
import time
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from io import BufferedReader
from logging import currentframe
from os.path import normcase
from typing import List, Optional, Iterator, Dict, Tuple, Any
from contracts import indent
import cbor2
import yaml
from networkx.drawing.nx_pydot import write_dot

from zuper_commons.fs import make_sure_dir_exists
from zuper_commons.types import check_isinstance
from contracts.utils import format_obs
from zuper_json.ipce import object_to_ipce, ipce_to_object
from zuper_json.json2cbor import read_next_either_json_or_cbor
from zuper_json.json_utils import encode_bytes_before_json_serialization, decode_bytes_before_json_deserialization
from zuper_nodes import InteractionProtocol, InputReceived, OutputProduced, Unexpected, LanguageChecker
from zuper_nodes.structures import TimingInfo, local_time, TimeSpec, timestamp_from_seconds, DecodingError, \
    ExternalProtocolViolation, NotConforming, ExternalTimeout
from . import logger, logger_interaction
from .meta_protocol import basic_protocol, SetConfig, ProtocolDescription, ConfigDescription, \
    BuildDescription, NodeDescription

__all__ = [
    'Context',
    'wrap_direct',
]


def wrap_direct(node, protocol, args: Optional[List[str]] = None):
    if args is None:
        args = sys.argv[1:]

    check_implementation(node, protocol)
    run_loop(node, protocol, args)


class Context(metaclass=ABCMeta):

    @abstractmethod
    def write(self, topic: str, data: Any, timing: TimingInfo = None, with_schema: bool = False):
        pass

    @abstractmethod
    def info(self, msg: str): pass

    @abstractmethod
    def debug(self, msg: str): pass

    @abstractmethod
    def warning(self, msg: str): pass

    @abstractmethod
    def error(self, msg: str): pass

    @abstractmethod
    def get_hostname(self):
        pass


class ConcreteContext(Context):
    protocol: InteractionProtocol

    def __init__(self, of, protocol, pc, node_name, tout: Dict[str, str], binary_out):
        self.of = of
        self.protocol = protocol
        self.pc = pc
        self.node_name = node_name
        self.hostname = socket.gethostname()
        self.tout = tout

        self.last_timing = None

        self.binary_out = binary_out

    def set_last_timing(self, timing: TimingInfo):
        self.last_timing = timing

    def get_hostname(self):
        return self.hostname

    def write(self, topic, data, timing=None, with_schema=False):
        if topic not in self.protocol.outputs:
            msg = f'Output channel "{topic}" not found in protocol; know {sorted(self.protocol.outputs)}.'
            raise Exception(msg)

        # logger.info(f'Writing output "{topic}".')

        klass = self.protocol.outputs[topic]
        if isinstance(klass, type):
            check_isinstance(data, klass)

        event = OutputProduced(topic)
        res = self.pc.push(event)
        if isinstance(res, Unexpected):
            msg = f'Unexpected output {topic}: {res}'
            logger.error(msg)
            return

        klass = self.protocol.outputs[topic]

        if isinstance(data, dict):
            data = ipce_to_object(data, {}, {}, expect_type=klass)

        if timing is None:
            timing = self.last_timing

        if timing is not None:
            s = time.time()
            if timing.received is None:
                # XXX
                time1 = timestamp_from_seconds(s)
            else:
                time1 = timing.received.time
            processed = TimeSpec(time=time1,
                                 time2=timestamp_from_seconds(s),
                                 frame='epoch',
                                 clock=socket.gethostname())
            timing.processed[self.node_name] = processed
            timing.received = None

        # timing = TimingInfo(acquired=acquired, processed=processed)
        m = {}
        m[FIELD_COMPAT] = [CUR_PROTOCOL]
        m[FIELD_TOPIC] = self.tout.get(topic, topic)
        m[FIELD_DATA] = object_to_ipce(data, {}, with_schema=with_schema)

        if timing is not None:
            m[FIELD_TIMING] = object_to_ipce(timing, {}, with_schema=False)
        self._write_raw(m)
        logger_interaction.debug(f'Written output "{topic}".')

    def _write_raw(self, json_data):
        if self.binary_out:
            j = cbor2.dumps(json_data)
            self.of.write(j)
            self.of.flush()
        else:
            json_data = encode_bytes_before_json_serialization(json_data)
            j = json.dumps(json_data) + '\n'
            j = j.encode('utf-8')
            self.of.write(j)
            self.of.flush()

    def log(self, s):
        prefix = f'{self.hostname}:{self.node_name}: '
        logger.info(prefix + s)

    def info(self, s):
        prefix = f'{self.hostname}:{self.node_name}: '
        logger.info(prefix + s)

    def debug(self, s):
        prefix = f'{self.hostname}:{self.node_name}: '
        logger.debug(prefix + s)

    def warning(self, s):
        prefix = f'{self.hostname}:{self.node_name}: '
        logger.warning(prefix + s)

    def error(self, s):
        prefix = f'{self.hostname}:{self.node_name}: '
        logger.error(prefix + s)


def get_translation_table(t: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    tout = {}
    tin = {}
    for t in t.split(','):
        ts = t.split(':')
        if ts[0] == 'in':
            tin[ts[1]] = ts[2]

        if ts[0] == 'out':
            tout[ts[1]] = ts[2]

    return tin, tout


def check_variables():
    for k, v in os.environ.items():
        if k.startswith('AIDO') and k not in KNOWN:
            msg = f'I do not expect variable "{k}" set in environment with value "{v}".'
            msg += ' I expect: %s' % ", ".join(KNOWN)
            logger.warn(msg)


from .constants import ENV_ENCODING_VALID, ENV_DATA_IN, KNOWN, ENV_DATA_OUT, ENV_TRANSLATE, ENV_ENCODING, \
    ENV_ENCODING_CBOR, ENV_ENCODING_JSON, ENV_META_OUT, ENV_META_IN, ENV_NAME, ENV_CONFIG, FIELD_DATA, FIELD_COMPAT, \
    CUR_PROTOCOL, FIELD_TOPIC, FIELD_TIMING


def run_loop(node, protocol: InteractionProtocol, args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()

    check_variables()

    data_in = os.environ.get(ENV_DATA_IN, '/dev/stdin')
    data_out = os.environ.get(ENV_DATA_OUT, '/dev/stdout')
    meta_in = os.environ.get(ENV_META_IN, None)
    meta_out = os.environ.get(ENV_META_OUT, None)
    default_name = os.environ.get(ENV_NAME, None)
    translate = os.environ.get(ENV_TRANSLATE, '')
    encoding = os.environ.get(ENV_ENCODING, ENV_ENCODING_JSON)
    config = os.environ.get(ENV_CONFIG, '{}')

    parser.add_argument('--data-in', default=data_in)
    parser.add_argument('--data-out', default=data_out)
    parser.add_argument('--meta-in', default=meta_in)
    parser.add_argument('--meta-out', default=meta_out)
    parser.add_argument('--name', default=default_name)
    parser.add_argument('--config', default=config)
    parser.add_argument('--translate', default=translate)
    parser.add_argument('--encoding', default=encoding)
    parser.add_argument('--loose', default=False, action='store_true')

    parsed = parser.parse_args(args)

    if not parsed.encoding in ENV_ENCODING_VALID:
        msg = f'I expected the encoding value "{parsed.encoding}" to be one of {ENV_ENCODING_VALID}'
        raise Exception(msg)  # XXX

    tin, tout = get_translation_table(parsed.translate)

    # expect in:name1:name2, out:name2:name1

    fin = parsed.data_in
    fout = parsed.data_out

    meta_in = parsed.meta_in or fin
    meta_out = parsed.meta_out or fout

    fi = open_for_read(fin)
    mi = fi if meta_in == fin else open_for_read(fin)

    fo = open_for_write(fout)
    mo = fo if meta_out == fout else open_for_write(meta_out)

    node_name = parsed.name or type(node).__name__

    binary_out = ENV_ENCODING_CBOR == parsed.encoding
    logger.name = node_name

    config = yaml.load(config, Loader=yaml.SafeLoader)
    try:
        loop(node_name, fi, fo, mi, mo, node, protocol, tin, tout, binary_out,
             config=config)
    except BaseException as e:
        msg = f'Error in node {node_name}'
        logger.error(f'Error in node {node_name}: \n{traceback.format_exc()}')
        raise Exception(msg) from e
    finally:
        fo.flush()
        fo.close()
        if fo is not mo:
            mo.flush()
            mo.close()
        fi.close()

import traceback


def open_for_read(fin, timeout=None):
    t0 = time.time()
    # first open reader file in case somebody is waiting for it
    while not os.path.exists(fin):
        delta = time.time() - t0
        if timeout is not None and (delta > timeout):
            msg = f'The file {fin} was not created before {timeout} seconds. I give up.'
            raise EnvironmentError(msg)
        logger_interaction.info(f'waiting for file {fin} to be created')
        time.sleep(1)

    logger_interaction.info(f'Opening input {fin}')
    fi = open(fin, 'rb', buffering=0)
    # noinspection PyTypeChecker
    fi = BufferedReader(fi, buffer_size=1)
    return fi


def open_for_write(fout):
    if fout == '/dev/stdout':
        return open('/dev/stdout', 'wb', buffering=0)
    else:
        wants_fifo = fout.startswith('fifo:')
        fout = fout.replace('fifo:', '')

        logger_interaction.info(f'Opening output file {fout} (wants fifo: {wants_fifo})')

        if not os.path.exists(fout):

            if wants_fifo:
                make_sure_dir_exists(fout)
                os.mkfifo(fout)
                logger_interaction.info('Fifo created.')
        else:
            is_fifo = stat.S_ISFIFO(os.stat(fout).st_mode)
            if wants_fifo and not is_fifo:
                logger_interaction.info(f'Recreating {fout} as a fifo.')
                os.unlink(fout)
                os.mkfifo(fout)

        if wants_fifo:
            logger_interaction.info('Fifo detected. Opening will block until a reader appears.')

        make_sure_dir_exists(fout)
        fo = open(fout, 'wb', buffering=0)

        if wants_fifo:
            logger_interaction.info('Reader has connected to my fifo')

        return fo


def loop(node_name, fi, fo, mi, mo, node, protocol, tin, tout, binary_out: bool,
         config: dict):
    logger.info(f'Starting reading')

    pc = LanguageChecker(protocol.interaction)
    pc2 = LanguageChecker(basic_protocol.interaction)
    if False:
        fn = 'language.dot'
        write_dot(pc2.g, fn)
        logger.info(f'Wrote graph to {fn}')

    context_data = ConcreteContext(of=fo, protocol=protocol, pc=pc, node_name=node_name, tout=tout,
                                   binary_out=binary_out)
    context_meta = ConcreteContext(of=mo, protocol=basic_protocol, pc=pc2, node_name=node_name + '.wrapper', tout=tout,
                                   binary_out=binary_out)
    initialized = False

    ATT_CONFIG = 'config'

    def set_config(key, value):
        if hasattr(node, ATT_CONFIG):
            config = node.config
            if hasattr(config, key):
                setattr(node.config, key, value)
            else:
                msg = f'Could not find config key {key}'
                raise ValueError(msg)

        else:
            msg = 'Node does not have the "config" attribute.'
            raise ValueError(msg)

    class Wrapper:
        def on_received_set_config(self, context, data: SetConfig):
            key = data.key
            value = data.value

            try:
                set_config(key, value)
            except ValueError as e:
                context.write('set_config_error', str(e))
            else:
                context.write('set_config_ack', None)

        def on_received_describe_protocol(self, context):
            desc = ProtocolDescription(data=protocol, meta=basic_protocol)
            context.write('protocol_description', desc)

        def on_received_describe_config(self, context):
            K = type(node)
            if hasattr(K, '__annotations__') and ATT_CONFIG in K.__annotations__:
                config_type = K.__annotations__[ATT_CONFIG]
                config_current = getattr(node, ATT_CONFIG)
            else:
                @dataclass
                class NoConfig:
                    pass

                config_type = NoConfig
                config_current = NoConfig()
            desc = ConfigDescription(config=config_type, current=config_current)
            context.write('config_description', desc, with_schema=True)

        def on_received_describe_node(self, context):
            desc = NodeDescription(node.__doc__)

            context.write('node_description', desc, with_schema=True)

        def on_received_describe_build(self, context):
            desc = BuildDescription()

            context.write('build_description', desc, with_schema=True)

    wrapper = Wrapper()

    for k, v in config.items():
        set_config(k, v)

    waiting_for = 'Expecting control message or one of:  %s' % pc.get_expected_events()

    try:
        for stream, parsed in inputs([fi, mi], waiting_for=waiting_for):
            topic = parsed[FIELD_TOPIC]
            topic = tin.get(topic, topic)
            parsed[FIELD_TOPIC] = topic
            logger_interaction.info(f'Received message of topic "{topic}".')
            if topic.startswith('wrapper.'):
                parsed[FIELD_TOPIC] = topic.replace('wrapper.', '')
                handle_message_node(parsed, basic_protocol, pc2, wrapper, context_meta)
            else:
                if not initialized:
                    try:
                        call_if_fun_exists(node, 'init', context=context_data)
                    except BaseException as e:
                        msg = "Exception while calling the node's init() function."
                        msg += '\n\n' + indent(traceback.format_exc(), '| ')
                        context_meta.write('aborted', msg)
                        raise Exception(msg) from e
                    initialized = True

                try:
                    handle_message_node(parsed, protocol, pc, node, context_data)
                except BaseException as e:
                    msg = f"Exception while handling a message on topic \"{topic}\"."
                    msg += '\n\n' + indent(traceback.format_exc(), '| ')
                    context_meta.write('aborted', msg)
                    raise Exception(msg) from e

    except StopIteration:
        pass
    except ExternalTimeout as e:
        msg = 'Could not receive any other messages.'
        msg += '\n Expecting one of:  %s' % pc.get_expected_events()
        raise ExternalTimeout(msg) from e

    res = pc.finish()
    if isinstance(res, Unexpected):
        msg = f'Protocol did not finish: {res}'
        logger_interaction.error(msg)

    if initialized:
        try:
            call_if_fun_exists(node, 'finish', context=context_data)
        except BaseException as e:
            msg = "Exception while calling the node's finish() function."
            msg += '\n\n' + indent(traceback.format_exc(), '| ')
            context_meta.write('aborted', msg)
            raise Exception(msg) from e

def handle_message_node(parsed, protocol, pc: LanguageChecker, agent, context):
    topic = parsed[FIELD_TOPIC]
    data = parsed[FIELD_DATA]

    if topic not in protocol.inputs:
        msg = f'Input channel "{topic}" not found in protocol. Known: {sorted(protocol.inputs)}'
        raise ExternalProtocolViolation(msg)

    klass = protocol.inputs[topic]
    try:
        data = decode_bytes_before_json_deserialization(data)
        ob = ipce_to_object(data, {}, {}, expect_type=klass)
    except BaseException as e:
        msg = f'Cannot deserialize object for topic "{topic}" expecting {klass}.'
        try:
            parsed = json.dumps(parsed, indent=2)
        except:
            parsed = str(parsed)
        msg += '\n\n' + contracts.indent(parsed, '|', 'parsed: |')
        raise DecodingError(msg) from e

    if parsed.get(FIELD_TIMING, None) is not None:
        timing = ipce_to_object(parsed[FIELD_TIMING], {}, {}, expect_type=TimingInfo)
    else:
        timing = TimingInfo()

    timing.received = local_time()

    context.set_last_timing(timing)
    # logger.info(f'Before push the state is\n{pc}')

    event = InputReceived(topic)
    expected = pc.get_expected_events()

    res = pc.push(event)

    # names = pc.get_active_states_names()
    # logger.info(f'After push of {event}: result \n{res} active {names}' )
    if isinstance(res, Unexpected):
        msg = f'Unexpected input "{topic}": {res}'
        msg += f'\nI expected: {expected}'
        msg += '\n' + format_obs(dict(pc=pc))
        logger.error(msg)
        raise ExternalProtocolViolation(msg)
    else:
        expect_fn = f'on_received_{topic}'
        call_if_fun_exists(agent, expect_fn, data=ob, context=context, timing=timing)


import select




def inputs(fs, give_up: Optional[float] = None, waiting_for: str = None) -> Iterator[Dict]:
    last = time.time()
    intermediate_timeout = 3.0
    intermediate_timeout_multiplier = 1.5
    while True:
        readyr, readyw, readyx = select.select(fs, [], fs, intermediate_timeout)
        if readyr:
            for fi in readyr:
                try:
                    parsed = read_next_either_json_or_cbor(fi, waiting_for=waiting_for)
                except StopIteration:
                    return

                if not isinstance(parsed, dict):
                    msg = f'Expected a dictionary, obtained {parsed!r}'
                    logger.error(msg)
                    continue

                if not FIELD_DATA in parsed:
                    parsed[FIELD_DATA] = None

                if not FIELD_COMPAT in parsed:
                    msg = f'Could not find field "compat" in structure "{parsed}".'
                    logger.error(msg)
                    continue

                l = parsed[FIELD_COMPAT]
                if not isinstance(l, list):
                    msg = f'Expected a list for compatibility value, found {l!r}'
                    logger.error(msg)
                    continue

                if not CUR_PROTOCOL in parsed[FIELD_COMPAT]:
                    msg = f'Skipping message because could not find {CUR_PROTOCOL} in {l}.'
                    logger.warn(msg)
                    continue

                # check fields

                yield fi, parsed
            else:
                continue
            break

        elif readyx:
            logger.warning('Exceptional condition on input channel %s' % readyx)
        else:
            delta = time.time() - last
            if give_up is not None and (delta > give_up):
                msg = f'I am giving up after %.1f seconds.' % delta
                raise ExternalTimeout(msg)
            else:
                intermediate_timeout *= intermediate_timeout_multiplier
                msg = f'Input channel not ready after %.1f seconds. Will re-try.' % delta
                if waiting_for:
                    msg += '\n' + contracts.indent(waiting_for, '> ')
                msg = 'I will warn again in %.1f seconds.' % intermediate_timeout
                logger.warning(msg)


import contracts


def call_if_fun_exists(ob, fname, **kwargs):
    kwargs = dict(kwargs)
    if not hasattr(ob, fname):
        msg = f'Missing function {fname}() for {contracts.describe_type(ob)}'
        logger.warning(msg)
        return
    f = getattr(ob, fname)
    a = inspect.getfullargspec(f)
    for k, v in dict(kwargs).items():
        if k not in a.args:
            kwargs.pop(k)
    try:
        f(**kwargs)
    except TypeError as e:
        msg = f'Cannot call function {f} with arguments {kwargs}.'
        msg += f'\n\nargspec: {a}'
        raise TypeError(msg) from e


def check_implementation(node, protocol: InteractionProtocol):
    logger.info('checking implementation')
    for n in protocol.inputs:
        expect_fn = f'on_received_{n}'
        if not hasattr(node, expect_fn):
            msg = f'Missing function {expect_fn}'
            msg += f'\nI know {sorted(type(node).__dict__)}'
            raise NotConforming(msg)

    for x in type(node).__dict__:
        if x.startswith('on_received_'):
            input_name = x.replace('on_received_', '')
            if input_name not in protocol.inputs:
                msg = f'The node has function "{x}" but there is no input "{input_name}".'
                raise NotConforming(msg)


def monkeypatch_findCaller():
    if __file__.lower()[-4:] in ['.pyc', '.pyo']:
        _wrapper_srcfile = __file__.lower()[:-4] + '.py'
    else:
        _wrapper_srcfile = __file__
    _wrapper_srcfile = normcase(_wrapper_srcfile)

    def findCaller(self, stack_info=False):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = normcase(co.co_filename)
            if filename == _wrapper_srcfile or filename == logging._srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    logging.Logger.findCaller = findCaller


monkeypatch_findCaller()
