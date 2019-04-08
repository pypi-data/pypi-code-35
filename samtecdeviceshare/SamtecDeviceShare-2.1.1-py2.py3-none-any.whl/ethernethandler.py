""" Ethernet Handler """
#!/usr/bin/env python
import os
import time
import logging; logger = logging.getLogger('samtecdeviceshare')  # pylint: disable=multiple-statements
try:
    import NetworkManager as NM
except ImportError as err:
    if os.getenv('PYTHON_ENV') == 'development':
        logger.warning('Failed to load NetworkManager module. Using emulator in development mode.')
        class NetworkManager:
            NM_DEVICE_STATE_ACTIVATED = 100
            NM_DEVICE_STATE_IP_CHECK = 80
            NM_DEVICE_STATE_IP_CONFIG = 70
            NM_DEVICE_STATE_FAILED = 120
            NM_DEVICE_STATE_UNAVAILABLE = 20
            NM_DEVICE_STATE_UNMANAGED = 10
            NM_DEVICE_TYPE_ETHERNET = 1
            def __init__(self):
                pass
            def nm_state(self):
                pass
        NM = NetworkManager
    else:
        logger.exception('Failed to load NetworkManager module with error: %s', err)
        raise err

# pylint: disable=too-many-instance-attributes
class EthernetHandler:
    CONN_STATES = ['DISCONNECTED', 'CONNECTING', 'CONNECTED']
    NM_CONNECTED_STATES = [NM.NM_DEVICE_STATE_ACTIVATED]
    NM_CONNECTING_STATES = [
        NM.NM_DEVICE_STATE_IP_CHECK,
        NM.NM_DEVICE_STATE_IP_CONFIG
    ]
    NM_DISCONNECTED_STATES = [
        NM.NM_DEVICE_STATE_FAILED,
        NM.NM_DEVICE_STATE_UNAVAILABLE,
        NM.NM_DEVICE_STATE_UNMANAGED
    ]

    def __init__(self, targetDev=None):
        self.DHCP_TIMEOUT = int(os.getenv('ETH_DHCP_TIMEOUT', '15'))
        self.LINK_LOCAL_TIMEOUT = int(os.getenv('ETH_LOCAL_TIMEOUT', '30'))
        self.targetDev = targetDev or os.getenv('ETH_TARGET_NAME')
        self.REFRESH_DELAY = 1
        self.devName = None
        self.devState = None
        self.conName = None
        self.conState = 'DISCONNECTED'
        self.conCounter = 0
        self.conNeedsInit = True

    def run(self):
        while True:
            try:
                self.update()
            except Exception as err:
                logger.exception('Received following exception: %s', err)
            finally:
                time.sleep(self.REFRESH_DELAY)

    def getWiredDevice(self):
        for dev in NM.NetworkManager.GetDevices():
            isEthernet = dev.DeviceType == NM.NM_DEVICE_TYPE_ETHERNET
            isTargetDevice = not self.targetDev or (self.targetDev and self.targetDev != dev.Interface)
            if isEthernet and isTargetDevice:
                return dev
        return None

    def getActiveWiredConnection(self):
        targetCon = None
        targetDev = None
        for act in NM.NetworkManager.ActiveConnections:
            try:
                settings = act.Connection.GetSettings()
                actCon = act.Connection
                actDevs = [d for d in act.Devices]
                # Skip if connection doesnt have 802-3-ethernet
                connType = settings['connection'].get('type', None)
                if connType != '802-3-ethernet' or '802-3-ethernet' not in settings.keys():
                    continue
                targetCon = actCon
                targetDev = None
                # Skip if no device
                if len(actDevs) != 1:
                    continue
                
                if self.targetDev and self.targetDev != actDevs[0].Interface:
                    logger.warning('Skipping connection %s as it doesnt match target: %s', actDevs[0], self.targetDev)
                    continue
                targetDev = actDevs[0]
                # Return first instance if has connection and device
                return targetCon, targetDev
            except Exception as err:
                logger.warning('Skipping active connection. Failed parsing with error: %s', err)

        return targetCon, targetDev

    def updateActiveWiredConnection(self, con=None, dev=None, method='auto'):
        success = False
        try:
            settings = con.GetSettings()
            # Add IPv4 setting if it doesn't yet exist
            if 'ipv4' not in settings:
                settings['ipv4'] = {}
            # Set the method and change properties
            settings['ipv4']['method'] = method
            settings['ipv4']['addresses'] = []
            con.Update(settings)
            con.Save()
            NM.NetworkManager.ActivateConnection(con, dev, "/")
            success = True
        except Exception:
            success = False
        return success

    def getDeviceState(self, dev):
        return dev.State

    def update(self):
        if os.environ.get('PYTHON_ENV') == 'development':
            return
        nextConName = None
        nextDevName = None
        nextDevState = None
        nextConMethod = None
        nextConState = None
        con, dev = self.getActiveWiredConnection()

        # Get device and connection name and state
        if con is None or dev is None:
            self.conNeedsInit = True
            dev = self.getWiredDevice()
            conSettings = None
            conMethod = 'auto'
            nextConName = 'Unknown'
            nextDevName = dev.Interface if dev else None
            nextDevState = self.getDeviceState(dev) if dev else NM.NM_DEVICE_STATE_UNAVAILABLE
        else:
            conSettings = con.GetSettings()
            conMethod = conSettings.get('ipv4', {}).get('method', '')
            nextConName = conSettings.get('connection', {}).get('id', '')
            nextDevName = dev.Interface
            nextDevState = self.getDeviceState(dev)

        # Determine whether to change connection method
        if nextDevState in EthernetHandler.NM_CONNECTED_STATES:
            self.conCounter = 0
            nextConState = 'CONNECTED'
            nextConMethod = conMethod
        elif nextDevState in EthernetHandler.NM_CONNECTING_STATES:
            nextConState = 'CONNECTING'
            # DHCP timeout, go to Link-Local
            if conMethod == 'auto' and self.conCounter >= self.DHCP_TIMEOUT:
                logger.info('auto method timeout. Switching to link-local')
                nextConMethod = 'link-local'
                self.conCounter = 0
            # Link-Local timeout, go to DHCP
            elif conMethod == 'link-local' and self.conCounter >= self.LINK_LOCAL_TIMEOUT:
                logger.info('link-local method timeout. Switching to auto')
                nextConMethod = 'auto'
                self.conCounter = 0
            else:
                nextConMethod = conMethod
                self.conCounter += 1

        elif nextDevState in EthernetHandler.NM_DISCONNECTED_STATES:
            self.conCounter = 0
            nextConState = 'DISCONNECTED'
            nextConMethod = 'auto'
        else:
            self.conCounter = self.conCounter
            nextConState = nextConState
            nextConMethod = conMethod

        if nextDevName != self.devName:
            logger.info('Wired device name changed to {0}'.format(nextDevName))
        if nextConName != self.conName:
            logger.info('Wired connection name changed to {0}'.format(nextConName))
        if nextConState != self.conState:
            logger.info('Wired connection state changed to {0}'.format(nextConState))

        # If have connection and want method to change or needs initialization
        if con and (self.conNeedsInit or (nextConMethod != conMethod)):
            # IMPORTANT: On init we must start with DHCP
            nextConMethod = 'auto' if self.conNeedsInit else nextConMethod
            logger.info('Setting connection {0} to method {1}'.format(nextConName, nextConMethod))
            success = self.updateActiveWiredConnection(con, dev, nextConMethod)
            # NOTE: If failed to activate, we'll retry next iteration
            if not success:
                nextConMethod = conMethod
                self.conNeedsInit = True
                logger.warning('Failed setting active connection method.')
            else:
                self.conNeedsInit = False
                logger.info('Successfully set active connection method.')
        self.devName = nextDevName
        self.devState = nextDevState
        self.conName = nextConName
        self.conState = nextConState

if __name__ == '__main__':
    handler = EthernetHandler()
    handler.run()
