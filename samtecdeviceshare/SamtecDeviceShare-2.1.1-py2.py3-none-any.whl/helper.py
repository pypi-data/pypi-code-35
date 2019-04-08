#!/usr/bin/env python
import os
import socket
import uuid
import time
import struct
import fcntl
import logging; logger = logging.getLogger('samtecdeviceshare') # pylint: disable=multiple-statements

try:
    import dbus
except ImportError as err:
    if os.getenv('PYTHON_ENV') == 'development':
        logger.warning('Failed to load dbus module. Using emulator in development mode.')
    else:
        logger.exception('Failed to load dbus module with error: %s', err)
        raise err

def isOnline(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def getIPAddress(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except Exception:
        return ''

# pylint: disable=too-many-arguments,too-many-locals
def setupWIFIHotSpot(ssid, passphrase, iface='wlan0', conUUID=None, action=None, timeout=10):
    if os.getenv('PYTHON_ENV') == 'development':
        print('Creating wifi hotspot {0} on iface {1}'.format(ssid, iface))
        return
    ssidBytes = dbus.ByteArray(ssid.encode("utf-8"))
    # If id is matched in setupWIFIConnection the UUID is replaced with previous
    wifiUUID = conUUID if conUUID else str(uuid.uuid4())
    # wifiUUID = conUUID if conUUID else '0cd1611e-942c-48b0-aa49-756a6a3818b7'
    wifiChannel = dbus.UInt32(1)
    s_con = dbus.Dictionary(dict(type='802-11-wireless', uuid=wifiUUID, id=ssid))
    s_wifi = dbus.Dictionary(dict(ssid=ssidBytes, mode='ap', band='bg', channel=wifiChannel))
    s_wsec = dbus.Dictionary({'key-mgmt': 'wpa-psk', 'proto': ['rsn'], 'psk': passphrase})
    s_ip4 = dbus.Dictionary(dict(method='shared'))
    s_ip6 = dbus.Dictionary(dict(method='ignore'))
    con = dbus.Dictionary({
        'connection': s_con,
        '802-11-wireless': s_wifi,
        '802-11-wireless-security': s_wsec,
        'ipv4': s_ip4,
        'ipv6': s_ip6
    })
    setupWIFIConnection(con, iface=iface, action=action, timeout=timeout)

# pylint: disable=too-many-arguments,too-many-locals
def setupWIFIClient(ssid, passphrase, identity=None, iface='wlan0', conUUID=None, action=None, timeout=10):
    if os.environ.get('PYTHON_ENV') == 'development':
        print('Creating wifi client {0} on iface {1}'.format(ssid, iface))
        return
    ssidBytes = dbus.ByteArray(ssid.encode("utf-8"))
    # If id is matched in setupWIFIConnection the UUID is replaced with previous
    wifiUUID = conUUID if conUUID else str(uuid.uuid4())
    s_con = dbus.Dictionary(dict(type='802-11-wireless', uuid=wifiUUID, id=ssid))
    s_wifi = dbus.Dictionary(dict(ssid=ssidBytes, security='802-11-wireless-security'))
    # WPA2 Enterprise pylint: disable=len-as-condition
    if isinstance(identity, str) and len(identity):
        s_wsec = dbus.Dictionary({'key-mgmt': 'wpa-eap', 'auth-alg': 'open'})
        s_eap = dbus.Dictionary({
            'eap': 'peap',
            'identity': identity,
            'phase2-auth': 'mschapv2',
            'password': passphrase
        })
    # WPA2 Regular
    else:
        s_wsec = dbus.Dictionary({'key-mgmt': 'wpa-psk', 'psk': passphrase, 'auth-alg': 'open'})
        s_eap = None
    s_ip4 = dbus.Dictionary({'method': 'auto'})
    s_ip6 = dbus.Dictionary({'method': 'auto'})
    con = dbus.Dictionary({
        'connection': s_con,
        '802-11-wireless': s_wifi,
        '802-11-wireless-security': s_wsec,
        'ipv4': s_ip4,
        'ipv6': s_ip6
    })
    if s_eap:
        con.update(dbus.Dictionary({'802-1x': s_eap}))
    setupWIFIConnection(con, iface=iface, action=action, timeout=timeout)

def setupWIFIConnection(con, iface='wlan0', action=None, timeout=10):
    try:
        bus = dbus.SystemBus()
        serviceName = "org.freedesktop.NetworkManager"
        proxy = bus.get_object(serviceName, "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

        proxy = bus.get_object(serviceName, "/org/freedesktop/NetworkManager")
        nm = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
        devPath = nm.GetDeviceByIpIface(iface)

        # Find our existing connection
        conPath = None
        conSettings = None
        config = None
        for path in settings.ListConnections():
            proxy = bus.get_object(serviceName, path)
            conSettings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings.Connection")
            config = conSettings.GetSettings()
            if config['connection']['id'] == con['connection']['id']:
                conPath = path
                break

        # If connection already exist, update it
        if conPath:
            con['connection']['uuid'] = config['connection']['uuid']
            conSettings.Update(con)
            conSettings.Save()
        # If connection doesnt exist, add it
        else:
            conPath = settings.AddConnection(con)

        # If no action, return
        if action is None:
            return

        # Now start or stop the connection on the requested device
        proxy = bus.get_object(serviceName, devPath)
        device = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Device")
        if str(action).upper() == 'UP':
            actPath = nm.ActivateConnection(conPath, devPath, "/")
            proxy = bus.get_object(serviceName, actPath)
            actProps = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
            time.sleep(0.5)
            # Wait for the connection to start up
            start = time.time()
            while time.time() < start + int(timeout):
                state = actProps.Get("org.freedesktop.NetworkManager.Connection.Active", "State")
                if state == 2:  # NM_ACTIVE_CONNECTION_STATE_ACTIVATED
                    return
                time.sleep(1)
            raise Exception('Failed to start wifi connection due to timeout')
        elif str(action).upper() == 'DOWN':
            device.Disconnect()
        else:
            raise Exception('Unsupported action')
    except Exception as err:
        raise err


if __name__ == "__main__":
    pass
