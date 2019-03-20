
from epsolar_tracer.Register import Register
from epsolar_tracer.Value import Value


class Coil(Register):
    def decode(self, response):
        if hasattr(response, "bits"):
            return Value(self, response.bits[0])
        return Value(self, None)
