import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import socket
import subprocess
from os.path import expanduser

base_dir = expanduser('~') + '/cloud/authMgr/'
sock_file = base_dir + "sock_file"
log_file = base_dir + "token_api.log"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

logger = logging.getLogger("Token_api")
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def open_socket(): #pragma: no cover
    global sock
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    try:
        sock.connect(sock_file)
    except socket.error, msg:
        logger.error("API: open_socket connect error %s" % msg)
        return (1, msg)
    return (0, sock)


def ping_server(sock):
    sock.settimeout(3)
    try:
        # Send data
        message = 'Ping'
        sock.sendall(message)

        # Receive the response
        data = sock.recv(8)
        if data == "Ack":
            return 0
        logger.error("API: ping_server: unexpected server response %s" % data)
        return 1

    except socket.timeout:
        logger.error("API: ping_server: socket timeout")
        return 2
    except socket.error as e:
        logger.error("API: ping_server: socket error %s" % str(e))
        return 3
    except Exception as e:
        logger.error("API: ping_server: other socket error %s" % str(e))
        return 4


def connect():
    global sock

    (rc, sock) = open_socket()
    if rc != 0:
        return rc

    rc = ping_server(sock)
    if rc != 0:
        logger.error("API: connect: ping failed")

    return rc


def send_message_to_server(message): # pragma: no cover
    global sock

    rc = connect()
    if rc != 0:
        logger.error("API: failed to connect to server")
        print "API: failed to connect to server"
        sys.exit(1)

    sock.settimeout(3)
    try:
        # Send data
        sock.sendall(message)

        # Receive the response
        data = sock.recv(80)

    except socket.timeout:
        logger.error("API: socket timeout")
        print "API: socket timeout"
    except socket.error:
        logger.error("API: socket error")
        print "API: socket error"
    except Exception as e:
        logger.error("API: other socket error %s" % str(e))
        print "API: other socket error %s" % str(e)

    disconnect()
    return data


def send_show_req_to_server(message): # pragma: no cover
    global sock

    rc = connect()
    if rc != 0:
        logger.error("API: failed to connect to server")
        print "API: failed to connect to server"
        sys.exit(1)

    sock.settimeout(3)
    buf = ''
    try:
        # Send data
        sock.sendall(message)

        # Receive the number of bytes in the token
        data = sock.recv(8)
        # Split the first response from the server
        two_str = data.rsplit('#')
        str_len = int(two_str[0])
        buf = two_str[1]

        # Now get the remaining bytes of the token
        total_bytes_received = len(two_str[1])
        while total_bytes_received < str_len:
            data = sock.recv(8)
            bytes_received = len(data)
            buf = buf + data
            total_bytes_received += bytes_received
        print "%s" % buf
        rc = 0

    except socket.timeout:
        logger.error("API: socket timeout")
        print "API: socket timeout"
        rc = 1
    except socket.error:
        logger.error("API: socket error")
        print "API: socket error"
        rc = 2
    except Exception as e:
        logger.error("API: other socket error %s" % str(e))
        print "API: other socket error %s" % str(e)
        rc = 3

    disconnect()
    return rc


def disconnect(): # pragma: no cover
    global sock
    sock.close()


def request_token_by_default_app(): # pragma: no cover
    global sock

    logger.info("Requesting token from default authentication application")
    token = ''
    token_len = 0
    total_bytes_received = 0
    try:
        # Send request message
        req_msg = "MSI_req"
        sock.sendall(req_msg)

        # Receive the number of bytes in the token
        data = sock.recv(8)
        # Split the first response from the server
        two_str = data.rsplit(' ')
        token_len = int(two_str[0])
        token = two_str[1]

        # Now get the remaining bytes of the token
        total_bytes_received = len(two_str[1])
        while total_bytes_received < token_len:
            data = sock.recv(8)
            bytes_received = len(data)
            token = token + data
            total_bytes_received += bytes_received

    except socket.timeout:
        logger.error("API: msi: socket timeout")
        logger.error("API: msi: expected token len %d" % token_len)
        logger.error("API: msi: actual token len %d" % total_bytes_received)
        token = ''
    except socket.error as e:
        logger.error("API: msi: socket error %s" % str(e))
        logger.error("API: msi: expected token len %d" % token_len)
        logger.error("API: msi: actual token len %d" % total_bytes_received)
        token = ''
    except Exception as e:
        logger.error("API: msi: other socket error %s" % str(e))
        logger.error("API: msi: expected token len %d" % token_len)
        logger.error("API: msi: actual token len %d" % total_bytes_received)
        token = ''

    finally:
        return token


def request_token_by_aad(cloud, tenantId, appId, appKey): #pragma: no cover
    global sock

    logger.info("Requesting token from specified AAD application")
    token = ''
    try:
        # Send request message
        req_msg = "AAD_req %s %s %s %s" % (cloud, tenantId, appId, appKey)
        sock.sendall(req_msg)

        # Receive the number of bytes in the token
        data = sock.recv(8)
        # Split the first response from the server
        two_str = data.rsplit(' ')
        token_len = int(two_str[0])
        token = two_str[1]
        token_len = token_len - len(two_str[1])

        # Now get the remaining bytes of the token
        total_bytes_received = 0
        while total_bytes_received < token_len:
            data = sock.recv(8)
            bytes_received = len(data)
            token = token + data
            total_bytes_received += bytes_received

    except socket.timeout:
        logger.error("API: aad: socket timeout")
        token = ''
    except socket.error as e:
        logger.error("API: aad: socket error %d" % str(e))
        token = ''
    except Exception as e:
        logger.error("API: aad: other socket error %d" % str(e))
        token = ''

    finally:
        return token


class Token_api():
    def __init__(self):
        if connect() != 0:
            subprocess.call(["sudo", "systemctl", "stop", "auth-token"])
            subprocess.call(["sudo", "systemctl", "start", "auth-token"])
            logger.error("Restarting the Token_svr")
            time.sleep(3)
            rc = connect()
            if rc != 0:
                logger.error("Unable to start the Token_svr")
                logger.error("Failed connection to Token Manager rc=%d" % rc)
                sys.exit()

    def set_default_aad_app(self, cloud, tenantId, appId, appKey):
        req_msg = "Set_app %s %s %s %s" % (cloud, tenantId, appId, appKey)
        return send_message_to_server(req_msg)

    def clear_default_aad_app(self):
        return send_message_to_server('Clear_app')

    def clear_aad_app_list(self):
        return send_message_to_server('Clear_list')

    def show_auth_apps(self):
        send_show_req_to_server('Show')
        return 'OK'

    def clear_token(self):
        return send_message_to_server('Clear_token')

    def refresh_token(self):
        return send_message_to_server('Refresh')

    def get_token_with_params(self, cloud, tenantId, appId, appKey):
        for attempt in range(3):
            rc = connect()
            if rc == 0:
                token = request_token_by_aad(cloud, tenantId, appId, appKey)

                if token == '':
                    logger.error("API: AAD: Failed to get token on attempt %d" % attempt)
                    disconnect()
                    if attempt < 3:
                        time.sleep(2)
                    else:
                        return token
                else:
                    disconnect()
                    break
            else:
                if attempt < 3:
                    time.sleep(2)
        else:
            return ''
        return token

    def get_token(self):
        for attempt in range(3):
            rc = connect()
            if rc == 0:
                token = request_token_by_default_app()

                if token == '':
                    logger.error("API: default: Failed to get token on attempt %d" % attempt)
                    disconnect()
                    if attempt < 3:
                        time.sleep(2)
                    else:
                        return token
                else:
                    disconnect()
                    break
            else:
                if attempt < 3:
                    time.sleep(2)
        else:
            return ''
        return token

    def disconnect(self): # pragma: no cover
        return disconnect()

    def is_server_up(self):
        return connect()


