#!/usr/bin/env python3.6

"""Random variable generator using quantum machines
"""
import random
import psutil
from pyquil.quil import Program
from pyquil import get_qc
from pyquil.gates import H, CNOT

BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF

def start_servers():
    """Checks if servers are running, if not starts them."""
    import os
    try:
        os.system("gnome-terminal -e 'qvm -S'")
        os.system("gnome-terminal -e 'quilc -S'")
    except:
        try:
            os.system("terminal -e 'qvm -S'")
            os.system("terminal -e 'quilc -S'")
        except:
            exit()

def bell_state():
    """Returns the Program object of a bell state operation on a quantum computer
    """
    return Program(H(0), CNOT(0, 1))

def arr_to_int(arr):
    """returns an integer from an array of binary numbers
    arr = [1 0 1 0 1 0 1] || [1,0,1,0,1,0,1]
    """
    return int(''.join([str(i) for i in arr]), 2)

def arr_to_bits(arr):
    """Returns a string of bits from an array"""
    return ''.join([str(i) for i in arr])

def int_to_bytes(k, bytesize=64):
    """returns a bytes object of the integer k with bytes"""
    return bytes(''.join(str(1 & int(k) >> i) for i in range(bytesize)[::-1]), 'utf-8')

def bits_to_bytes(k):
    """returns a bytes object of the bitstring k"""
    return int(k, 2).to_bytes((len(k) + 7) // 8, 'big')

def qvm():
    """Returns the quantum computer or virtual machine"""
    return get_qc('9q-square-qvm')

def test_quantum_connection():
    """
    Tests the connection to the quantum virtual machine.
    attempts to start the virtual machine if possible
    """
    while True:
        qvm_running = False
        quilc_running = False
        for proc in psutil.process_iter():
            if 'qvm' in proc.name().lower():
                qvm_running = True
            elif 'quilc' in proc.name().lower():
                quilc_running = True
        if qvm_running is False or quilc_running is False:
            try:
                start_servers()
            except Exception as exception:
                raise Exception(exception)
        else:
            break

class QRandom(random.Random):
    """Quantum random number generator

        Generates a random number by collapsing bell states on a
        quantum computer or quantum virtual machine.
    """

    def __init__(self):
        super().__init__(self)
        self.program = bell_state()
        self.qvm = qvm()
        test_quantum_connection()

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        return (int.from_bytes(self.getrandbits(56, 'bytes'), 'big') >> 3) * RECIP_BPF

    def getrandbits(self, k, x="int"):
        """getrandbits(k) -> x. generates an integer with k random bits"""
        if k <= 0:
            raise ValueError("Number of bits should be greater than 0")
        if k != int(k):
            raise ValueError("Number of bits should be an integer")
        out = bits_to_bytes(arr_to_bits(self.qvm.run_and_measure(self.program, trials=k)[0]))
        if x in ('int', 'INT'):
            return int.from_bytes(out, 'big')
        elif x in ('bytes', 'b'):
            return out
        else:
            raise ValueError(str(x) + ' not a valid type (int, bytes)')
