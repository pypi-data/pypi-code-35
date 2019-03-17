import hashlib
import logging
import random
import socket
import sys
import time

from esphome.core import EsphomeError
from esphome.helpers import is_ip_address, resolve_ip_address
from esphome.py_compat import IS_PY2, char_to_byte

RESPONSE_OK = 0
RESPONSE_REQUEST_AUTH = 1

RESPONSE_HEADER_OK = 64
RESPONSE_AUTH_OK = 65
RESPONSE_UPDATE_PREPARE_OK = 66
RESPONSE_BIN_MD5_OK = 67
RESPONSE_RECEIVE_OK = 68
RESPONSE_UPDATE_END_OK = 69

RESPONSE_ERROR_MAGIC = 128
RESPONSE_ERROR_UPDATE_PREPARE = 129
RESPONSE_ERROR_AUTH_INVALID = 130
RESPONSE_ERROR_WRITING_FLASH = 131
RESPONSE_ERROR_UPDATE_END = 132
RESPONSE_ERROR_INVALID_BOOTSTRAPPING = 133
RESPONSE_ERROR_WRONG_CURRENT_FLASH_CONFIG = 134
RESPONSE_ERROR_WRONG_NEW_FLASH_CONFIG = 135
RESPONSE_ERROR_ESP8266_NOT_ENOUGH_SPACE = 136
RESPONSE_ERROR_ESP32_NOT_ENOUGH_SPACE = 137
RESPONSE_ERROR_UNKNOWN = 255

OTA_VERSION_1_0 = 1

MAGIC_BYTES = [0x6C, 0x26, 0xF7, 0x5C, 0x45]

_LOGGER = logging.getLogger(__name__)


class ProgressBar(object):
    def __init__(self):
        self.last_progress = None

    def update(self, progress):
        bar_length = 60
        status = ""
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        new_progress = int(progress * 100)
        if new_progress == self.last_progress:
            return
        self.last_progress = new_progress
        block = int(round(bar_length * progress))
        text = "\rUploading: [{0}] {1}% {2}".format("=" * block + " " * (bar_length - block),
                                                    new_progress, status)
        sys.stderr.write(text)
        sys.stderr.flush()

    # pylint: disable=no-self-use
    def done(self):
        sys.stderr.write('\n')
        sys.stderr.flush()


class OTAError(EsphomeError):
    pass


def recv_decode(sock, amount, decode=True):
    data = sock.recv(amount)
    if not decode:
        return data
    return [char_to_byte(x) for x in data]


def receive_exactly(sock, amount, msg, expect, decode=True):
    if decode:
        data = []
    elif IS_PY2:
        data = ''
    else:
        data = b''

    try:
        data += recv_decode(sock, 1, decode=decode)
    except socket.error as err:
        raise OTAError("Error receiving acknowledge {}: {}".format(msg, err))

    try:
        check_error(data, expect)
    except OTAError as err:
        sock.close()
        raise OTAError("Error {}: {}".format(msg, err))

    while len(data) < amount:
        try:
            data += recv_decode(sock, amount - len(data), decode=decode)
        except socket.error as err:
            raise OTAError("Error receiving {}: {}".format(msg, err))
    return data


def check_error(data, expect):
    if not expect:
        return
    dat = data[0]
    if dat == RESPONSE_ERROR_MAGIC:
        raise OTAError("Error: Invalid magic byte")
    if dat == RESPONSE_ERROR_UPDATE_PREPARE:
        raise OTAError("Error: Couldn't prepare flash memory for update. Is the binary too big? "
                       "Please try restarting the ESP.")
    if dat == RESPONSE_ERROR_AUTH_INVALID:
        raise OTAError("Error: Authentication invalid. Is the password correct?")
    if dat == RESPONSE_ERROR_WRITING_FLASH:
        raise OTAError("Error: Wring OTA data to flash memory failed. See USB logs for more "
                       "information.")
    if dat == RESPONSE_ERROR_UPDATE_END:
        raise OTAError("Error: Finishing update failed. See the MQTT/USB logs for more "
                       "information.")
    if dat == RESPONSE_ERROR_INVALID_BOOTSTRAPPING:
        raise OTAError("Error: Please press the reset button on the ESP. A manual reset is "
                       "required on the first OTA-Update after flashing via USB.")
    if dat == RESPONSE_ERROR_WRONG_CURRENT_FLASH_CONFIG:
        raise OTAError("Error: ESP has been flashed with wrong flash size. Please choose the "
                       "correct 'board' option (esp01_1m always works) and then flash over USB.")
    if dat == RESPONSE_ERROR_WRONG_NEW_FLASH_CONFIG:
        raise OTAError("Error: ESP does not have the requested flash size (wrong board). Please "
                       "choose the correct 'board' option (esp01_1m always works) and try again.")
    if dat == RESPONSE_ERROR_ESP8266_NOT_ENOUGH_SPACE:
        raise OTAError("Error: ESP does not have enough space to store OTA file. Please try "
                       "flashing a minimal firmware (see FAQ)")
    if dat == RESPONSE_ERROR_ESP32_NOT_ENOUGH_SPACE:
        raise OTAError("Error: The OTA partition on the ESP is too small. ESPHome needs to resize "
                       "this partition, please flash over USB.")
    if dat == RESPONSE_ERROR_UNKNOWN:
        raise OTAError("Unknown error from ESP")
    if not isinstance(expect, (list, tuple)):
        expect = [expect]
    if dat not in expect:
        raise OTAError("Unexpected response from ESP: 0x{:02X}".format(data[0]))


def send_check(sock, data, msg):
    try:
        if IS_PY2:
            if isinstance(data, (list, tuple)):
                data = ''.join([chr(x) for x in data])
            elif isinstance(data, int):
                data = chr(data)
        else:
            if isinstance(data, (list, tuple)):
                data = bytes(data)
            elif isinstance(data, int):
                data = bytes([data])
            elif isinstance(data, str):
                data = data.encode('utf8')

        sock.sendall(data)
    except socket.error as err:
        raise OTAError("Error sending {}: {}".format(msg, err))


def perform_ota(sock, password, file_handle, filename):
    file_md5 = hashlib.md5(file_handle.read()).hexdigest()
    file_size = file_handle.tell()
    _LOGGER.info('Uploading %s (%s bytes)', filename, file_size)
    file_handle.seek(0)
    _LOGGER.debug("MD5 of binary is %s", file_md5)

    # Enable nodelay, we need it for phase 1
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    send_check(sock, MAGIC_BYTES, 'magic bytes')

    _, version = receive_exactly(sock, 2, 'version', RESPONSE_OK)
    if version != OTA_VERSION_1_0:
        raise OTAError("Unsupported OTA version {}".format(version))

    # Features
    send_check(sock, 0x00, 'features')
    receive_exactly(sock, 1, 'features', RESPONSE_HEADER_OK)

    auth, = receive_exactly(sock, 1, 'auth', [RESPONSE_REQUEST_AUTH, RESPONSE_AUTH_OK])
    if auth == RESPONSE_REQUEST_AUTH:
        if not password:
            raise OTAError("ESP requests password, but no password given!")
        nonce = receive_exactly(sock, 32, 'authentication nonce', [], decode=False)
        if not IS_PY2:
            nonce = nonce.decode()
        _LOGGER.debug("Auth: Nonce is %s", nonce)
        cnonce = hashlib.md5(str(random.random()).encode()).hexdigest()
        _LOGGER.debug("Auth: CNonce is %s", cnonce)

        send_check(sock, cnonce, 'auth cnonce')

        result_md5 = hashlib.md5()
        result_md5.update(password.encode())
        result_md5.update(nonce.encode())
        result_md5.update(cnonce.encode())
        result = result_md5.hexdigest()
        _LOGGER.debug("Auth: Result is %s", result)

        send_check(sock, result, 'auth result')
        receive_exactly(sock, 1, 'auth result', RESPONSE_AUTH_OK)

    file_size_encoded = [
        (file_size >> 24) & 0xFF,
        (file_size >> 16) & 0xFF,
        (file_size >> 8) & 0xFF,
        (file_size >> 0) & 0xFF,
    ]
    send_check(sock, file_size_encoded, 'binary size')
    receive_exactly(sock, 1, 'binary size', RESPONSE_UPDATE_PREPARE_OK)

    send_check(sock, file_md5, 'file checksum')
    receive_exactly(sock, 1, 'file checksum', RESPONSE_BIN_MD5_OK)

    # Disable nodelay for transfer
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
    # Limit send buffer (usually around 100kB) in order to have progress bar
    # show the actual progress
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)

    offset = 0
    progress = ProgressBar()
    while True:
        chunk = file_handle.read(1024)
        if not chunk:
            break
        offset += len(chunk)

        try:
            sock.sendall(chunk)
        except socket.error as err:
            sys.stderr.write('\n')
            raise OTAError("Error sending data: {}".format(err))

        progress.update(offset / float(file_size))
    progress.done()

    # Enable nodelay for last checks
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    _LOGGER.info("Waiting for result...")

    receive_exactly(sock, 1, 'receive OK', RESPONSE_RECEIVE_OK)
    receive_exactly(sock, 1, 'Update end', RESPONSE_UPDATE_END_OK)
    send_check(sock, RESPONSE_OK, 'end acknowledgement')

    _LOGGER.info("OTA successful")

    # Do not connect logs until it is fully on
    time.sleep(1)


def run_ota_impl_(remote_host, remote_port, password, filename):
    if is_ip_address(remote_host):
        _LOGGER.info("Connecting to %s", remote_host)
        ip = remote_host
    else:
        _LOGGER.info("Resolving IP address of %s", remote_host)
        try:
            ip = resolve_ip_address(remote_host)
        except EsphomeError as err:
            _LOGGER.error("Error resolving IP address of %s. Is it connected to WiFi?",
                          remote_host)
            _LOGGER.error("(If this error persists, please set a static IP address: "
                          "https://esphome.io/components/wifi.html#manual-ips)")
            raise OTAError(err)
        _LOGGER.info(" -> %s", ip)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    try:
        sock.connect((ip, remote_port))
    except socket.error as err:
        sock.close()
        _LOGGER.error("Connecting to %s:%s failed: %s", remote_host, remote_port, err)
        return 1

    file_handle = open(filename, 'rb')
    try:
        perform_ota(sock, password, file_handle, filename)
    except OTAError as err:
        _LOGGER.error(str(err))
        return 1
    finally:
        sock.close()
        file_handle.close()

    return 0


def run_ota(remote_host, remote_port, password, filename):
    try:
        return run_ota_impl_(remote_host, remote_port, password, filename)
    except OTAError as err:
        _LOGGER.error(err)
        return 1


def run_legacy_ota(verbose, host_port, remote_host, remote_port, password, filename):
    from esphome import espota

    espota_args = ['espota.py', '--debug', '--progress', '-i', remote_host,
                   '-p', str(remote_port), '-f', filename,
                   '-a', password, '-P', str(host_port)]
    if verbose:
        espota_args.append('-d')
    return espota.main(espota_args)
