"""Scan for mithermometer devices"""

# use only lower case names here
VALID_DEVICE_NAMES = ['mj_ht_v1']

DEVICE_PREFIX = '4C:65:A8:'


def scan(backend, timeout=10):
    """Scan for mithermometer devices.

    Note: this must be run as root!
    """
    result = []
    for (mac, name) in backend.scan_for_devices(timeout):
        if (name is not None and name.lower() in VALID_DEVICE_NAMES) or \
                mac is not None and mac.upper().startswith(DEVICE_PREFIX):
            result.append(mac.upper())
    return result
