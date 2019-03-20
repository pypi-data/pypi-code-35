class Value:
    """Value with unit"""

    def __init__(self, register, value):
        self.register = register
        if self.register.times != 1 and value is not None:
            self.value = 1.0 * value / self.register.times
        else:
            self.value = value

    def __str__(self):
        if self.value is None:
            return self.register.name + " = " + str(self.value)
        return self.register.name + " = " + str(self.value) + self.register.unit()[1]

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)
