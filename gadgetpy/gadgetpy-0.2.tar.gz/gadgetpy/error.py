# Basic Gadget Exception
class GadgetException(Exception):
    pass

# Attempting to create an existing gadget.  Need to remove the old one first.
class GadgetExists(GadgetException):
    pass

class GadgetInvalid(GadgetException):
    pass

# Attempting to update a gadget when it is already mounted.  Unmount it first.
class GadgetMounted(GadgetException):
    pass

# Attempting to mount a gadget to a pointer that either already is mounted,
# or doesn't exist
class PointerMounted(GadgetException):
    pass
