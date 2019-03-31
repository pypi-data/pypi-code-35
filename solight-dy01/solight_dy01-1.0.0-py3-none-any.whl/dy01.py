import pigpio
import time

class DY01:
    """
    Handles controlling of Solight DY01 sockets.
    """

    def __init__(self, pi, pin, transmit_time = 0.15):
        """
        Constructs the instance. Args:
        * pi - connection to pigpio daemon
        * pin - BCM pin number of GPIO
        * transmit_time (optional) - how many seconds command should be
          transmitted. It was experimentally found that 0.15 is probably lowest
          reliable value and this is the default. Setting lower value may cause
          the socket to miss commands. Set higher value if it's still
          unreliable for you. If the value is too big, it will slow down your
          program.
        """

        pi.set_mode(pin, pigpio.OUTPUT)
        self.pi = pi
        self.pin = pin
        self.transmit_time = transmit_time

    def send(self, address, action):
        """
        Transmits the command. Args:
        * address - 10 bit address of the socket.
        * action - 1 - turn on or 0 - turn off
        """
        def add_bit(wf, pin, bit):
            wf.append(pigpio.pulse(1 << pin, 0, 150 + 300*bit))
            wf.append(pigpio.pulse(0, 1 << pin, 450 - 300*bit))

        self.pi.wave_clear()
        # Safety measure
        if action != 0:
            action = 1

        wf = [pigpio.pulse(0, 1 << self.pin, 4600)]

        for _ in range(5):
            add_bit(wf, self.pin, (address >> 9) & 1)
            add_bit(wf, self.pin, 1)
            address <<= 1

        add_bit(wf, self.pin, 0)

        for _ in range(5):
            add_bit(wf, self.pin, (address >> 9) & 1)
            add_bit(wf, self.pin, 0)
            address <<= 1

        add_bit(wf, self.pin, action)
        add_bit(wf, self.pin, 0)
        if action == 0:
            add_bit(wf, self.pin, 1)
        else:
            add_bit(wf, self.pin, 0)

        add_bit(wf, self.pin, 0)

        self.pi.wave_add_generic(wf)
        wid = self.pi.wave_create()

        self.pi.wave_send_repeat(wid)
        time.sleep(self.transmit_time)
        self.pi.wave_tx_stop()
