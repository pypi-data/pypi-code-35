# -*- coding: utf-8 -*-
# XXX Update Docstring
"""
pyFuckery - test_vm.py
Created on 2/12/17.


"""
# Stdlib
import io
import logging
import os
# Third party code
import pytest

# Custom code
from fuckery.exc import VMError
from fuckery.parser import parse_program
from fuckery.vm import VirtualMachine

# Logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s [%(filename)s:%(funcName)s]')
log = logging.getLogger(__name__)

# Assets Configuration
ASSETS = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'assets')
assert os.path.isdir(ASSETS)


def get_file(fn) -> str:
    fp = os.path.join(ASSETS, fn)
    assert os.path.isfile(fp)
    return fp


def get_fn_contents(fn) -> bytes:
    fp = get_file(fn=fn)
    with open(fp, 'rb') as f:
        buf = f.read()
    return buf


@pytest.fixture()
def test_vm():
    vm = VirtualMachine()
    assert vm.data_pointer == 0
    return vm


class TestVm:

    def test_simple_vm(self):
        n = 20
        vm = VirtualMachine(memory_size=n)
        assert isinstance(vm, VirtualMachine)
        assert len(vm.memory) == n
        assert vm.data_pointer == 0

    def test_data_inc(self, test_vm: VirtualMachine):
        e = 1
        test_vm.inc_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == e

        test_vm.inc_data_value()
        test_vm.inc_data_value()
        test_vm.inc_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 4

        # Make sure things roll over
        test_vm.data_pointer = 1
        for _ in range(255):
            test_vm.inc_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 255
        test_vm.inc_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 0
        test_vm.inc_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 1

    def test_data_dec(self, test_vm: VirtualMachine):
        e = 255
        test_vm.dec_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == e

        test_vm.dec_data_value()
        test_vm.dec_data_value()
        test_vm.dec_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 252

        # Make sure things roll over
        test_vm.data_pointer = 1
        for _ in range(255):
            test_vm.dec_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 1
        test_vm.dec_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 0
        test_vm.dec_data_value()
        r = test_vm.memory.get(test_vm.data_pointer)
        assert r == 255

    def test_ptr_inc(self, test_vm: VirtualMachine):
        e = 1
        current_v = test_vm.data_pointer
        test_vm.inc_data_ptr()
        assert test_vm.data_pointer == e
        assert test_vm.data_pointer != current_v
        assert test_vm.data_pointer > current_v
        test_vm.inc_data_ptr()
        assert test_vm.data_pointer == e + 1
        test_vm.data_pointer = 0
        for i in range(test_vm._memory_size - 1):
            test_vm.inc_data_ptr()
        assert test_vm.data_pointer in test_vm.memory
        assert test_vm.data_pointer+1 not in test_vm.memory

        with pytest.raises(VMError) as cm:
            test_vm.inc_data_ptr()
        assert 'Invalid memory address' in str(cm.value)

    def test_ptr_dec(self, test_vm: VirtualMachine):
        with pytest.raises(VMError) as cm:
            test_vm.dec_data_ptr()
        assert 'Invalid memory address' in str(cm.value)

        test_vm.data_pointer = test_vm._memory_size - 1
        current_v = test_vm.data_pointer
        test_vm.dec_data_ptr()
        assert test_vm.data_pointer == (test_vm._memory_size - 2)
        assert test_vm.data_pointer != current_v
        assert test_vm.data_pointer < current_v

    def test_input_stream(self, test_vm: VirtualMachine):
        stream_in = io.StringIO('Hello World!\n')
        test_vm.stream_in = stream_in

        test_vm.io_input()
        assert test_vm.current_value == ord('H')
        for c in 'ello World!\n':
            test_vm.io_input()
            assert test_vm.current_value == ord(c)

        # XXX This raises a TypeError with ord....which is probably better handled somehow as a EOL character.
        # test_vm.io_input()


class TestExecution:

    def test_add(self, test_vm: VirtualMachine):
        # The add.bf program won't do anything since the loop will not be entered.
        fn = 'add.bf'
        buf = get_fn_contents(fn=fn)
        bf = buf.decode()
        tree = parse_program(s=bf)
        test_vm.stream_out = io.StringIO()
        sh = test_vm.memory.mem_hash
        test_vm.run(tree)
        assert test_vm.memory.mem_hash == sh

    def test_hello_world(self, test_vm: VirtualMachine):
        fn = 'hello_world.bf'
        buf = get_fn_contents(fn=fn)
        bf = buf.decode()
        tree = parse_program(s=bf)
        test_vm.stream_out = io.StringIO()
        test_vm.run(tree)
        test_vm.stream_out.seek(0)
        r = test_vm.stream_out.read()
        assert r == 'Hello World!\n'

    def test_minimal_hello_world(self, test_vm: VirtualMachine):
        # Minimal hello world from wikipedia
        s = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
        tree = parse_program(s=s)
        test_vm.stream_out = io.StringIO()
        test_vm.run(tree)
        test_vm.stream_out.seek(0)
        r = test_vm.stream_out.read()
        assert r == 'Hello World!\n'

    def test_minimal_hello_world_loop_detection(self, test_vm: VirtualMachine):
        # Minimal hello world from wikipedia
        s = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
        tree = parse_program(s=s)
        test_vm.stream_out = io.StringIO()
        # Enable loop detection.  This increases runtime at the expense of checking for infinite loops.
        test_vm.loop_detection = True
        test_vm.run(tree)
        test_vm.stream_out.seek(0)
        r = test_vm.stream_out.read()
        assert r == 'Hello World!\n'

    def test_loop_detection(self, test_vm: VirtualMachine):
        s = '+[+-]'
        tree = parse_program(s=s)
        test_vm.loop_detection = True
        with pytest.raises(VMError) as cm:
            test_vm.run(tree)
        assert 'Infinite loop detected - no change in memory during loop execution!' in str(cm.value)

    def test_parse_and_run(self, test_vm: VirtualMachine):
        # Minimal hello world from wikipedia
        s = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
        test_vm.stream_out = io.StringIO()
        test_vm.parse_and_run(program=s)
        test_vm.stream_out.seek(0)
        r = test_vm.stream_out.read()
        assert r == 'Hello World!\n'
