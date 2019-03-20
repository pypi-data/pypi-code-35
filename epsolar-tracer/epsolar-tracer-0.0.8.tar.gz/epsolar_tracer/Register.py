
from epsolar_tracer.Value import Value


class Register:
    def __init__(self, name: str, address: int, description: str, unit, times: int, size: int=1):
        self.name = name
        self.address = address
        self.description = description
        self.unit = unit
        self.times = times
        self.size = size

    def is_coil(self):
        return self.address < 0x1000

    def is_discrete_input(self) -> bool:
        return self.address >= 0x1000 and self.address < 0x3000

    def is_input_register(self) -> bool:
        return self.address >= 0x3000 and self.address < 0x9000

    def is_holding_register(self) -> bool:
        return self.address >= 0x9000

    def decode(self, response):
        if hasattr(response, "getRegister"):
            mask = rawvalue = lastvalue = 0
            for i in range(self.size):
                lastvalue = response.getRegister(i)
                rawvalue = rawvalue | (lastvalue << (i * 16))
                mask = (mask << 16) | 0xffff
            if (lastvalue & 0x8000) == 0x8000:
                # print rawvalue
                rawvalue = -(rawvalue ^ mask) - 1
            return Value(self, rawvalue)
        return Value(self, None)

    def encode(self, value: int) -> int:
        # FIXME handle 2 word registers
        rawvalue = int(value * self.times)
        if rawvalue < 0:
            rawvalue = (-rawvalue - 1) ^ 0xffff
            # print rawvalue
        return rawvalue
