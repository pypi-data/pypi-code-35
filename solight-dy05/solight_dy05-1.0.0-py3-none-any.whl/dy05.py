import pigpio
import time

class DY05:
    """
    Handles controlling Solight DY05 sockets.
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

    def send(self, address, socket, action):
        """
        Transmits the command. Args:
        * address - 20 bit address of the socket group.
        * socket - socket number 1-4. Any other value means "all in group"
        * action - 1 - turn on or 0 - turn off
        """
        def add_bit(wf, pin, bit):
            if bit == 0:
                wf.append(pigpio.pulse(1 << pin, 0, 340))
                wf.append(pigpio.pulse(0, 1 << pin, 840))
            else:
                wf.append(pigpio.pulse(1 << pin, 0, 840))
                wf.append(pigpio.pulse(0, 1 << pin, 340))

        def add_byte(wf, pin, byte):
            for _ in range(8):
                add_bit(wf, pin, byte & 128)
                byte <<= 1

        self.pi.wave_clear()
        # Safety measure
        if action != 0:
            action = 1

        wf = [pigpio.pulse(0, 1 << self.pin, 9600)]
        add_byte(wf, self.pin, address >> 12)
        add_byte(wf, self.pin, address >> 4)

        last_byte = (address << 4) & 0xF0

        if socket == 1:
            add_byte(wf, self.pin, (last_byte | 0x0E) + action)
        elif socket == 2:
            add_byte(wf, self.pin, (last_byte | 0x0C) + action)
        elif socket == 3:
            add_byte(wf, self.pin, (last_byte | 0x0A) + action)
        elif socket == 4:
            add_byte(wf, self.pin, (last_byte | 0x06) + action)
        else:
            add_byte(wf, self.pin, (last_byte | 0x01) + action)

        add_bit(wf, self.pin, 0)

        self.pi.wave_add_generic(wf)
        wid = self.pi.wave_create()

        self.pi.wave_send_repeat(wid)
        time.sleep(self.transmit_time)
        self.pi.wave_tx_stop()
