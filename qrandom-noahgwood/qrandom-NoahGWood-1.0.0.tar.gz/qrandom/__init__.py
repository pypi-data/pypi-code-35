from .qrandom import QRandom
name="qrandom"

__all__ = ["QRandom", "random", "randint", "randrange", "getstate", "setstate", "getrandbits"]

_inst = QRandom()
random = _inst.random
randint = _inst.randint
randrange = _inst.randrange
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits

