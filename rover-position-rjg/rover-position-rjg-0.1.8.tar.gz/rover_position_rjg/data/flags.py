class Flags:
    """A set of 8 boolean flags"""
    MAX_BITS = 8

    def __init__(self, initial_value: int = 0):
        if initial_value < 0 or initial_value >= (1 << Flags.MAX_BITS):
            raise ValueError('Initial value must be a positive {} bit integer'.format(Flags.MAX_BITS))
        self.data = initial_value

    def __getitem__(self, item: int) -> bool:
        self._check_index(item)
        return self.data & (1 << item) != 0

    def __setitem__(self, key: int, value: bool) -> None:
        self._check_index(key)
        if value:
            self.data = self.data | (1 << key)
        else:
            self.data = self.data & ~(1 << key)

    def __str__(self):
        return '0x{:02X}'.format(self.data)

    def __repr__(self) -> str:
        return str(self)

    def __int__(self) -> int:
        return self.data

    def __eq__(self, other):
        if type(other) != Flags:
            return False
        return self.data == other.data

    @staticmethod
    def _check_index(index: int):
        if index < 0 or index > Flags.MAX_BITS - 1:
            raise IndexError('Index must be between 0 and {} bits'.format(Flags.MAX_BITS))